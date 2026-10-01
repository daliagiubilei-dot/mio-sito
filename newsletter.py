"""Iscrizione alla newsletter: salvataggio nel database + invio a Mailchimp (se configurato).

Mailchimp usa l'interfaccia web (HTTPS), quindi funziona anche sul piano Hobby di Railway.
L'iscrizione parte in modalità "pending": Mailchimp manda l'email di conferma (doppio consenso) e la persona
entra nell'elenco solo dopo aver cliccato. È la forma più prudente dal punto di vista GDPR.
"""
import base64
import hashlib
import json
import logging
import re
import urllib.error
import urllib.request

from config import Config

log = logging.getLogger("daliamae.newsletter")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")

# Versione del testo di consenso mostrato nel modulo: si salva insieme all'iscrizione come prova.
CONSENT_VERSION = "newsletter-v1"
CONSENT_TEXT = ("Acconsento a ricevere la newsletter di Daliamae all'indirizzo indicato e ho letto l'informativa "
                "privacy. Posso annullare l'iscrizione in qualsiasi momento.")


def mailchimp_ready():
    return bool(Config.MAILCHIMP_API_KEY and "-" in Config.MAILCHIMP_API_KEY and Config.MAILCHIMP_LIST_ID)


def subscribe_mailchimp(email):
    """Ritorna (ok, stato, errore). `stato` è una parola breve da mostrare nel pannello."""
    if not mailchimp_ready():
        return False, "non collegato", ""
    dc = Config.MAILCHIMP_API_KEY.rsplit("-", 1)[1]
    h = hashlib.md5(email.lower().encode("utf-8")).hexdigest()
    url = "https://%s.api.mailchimp.com/3.0/lists/%s/members/%s" % (dc, Config.MAILCHIMP_LIST_ID, h)
    payload = {"email_address": email, "status_if_new": "pending", "language": "it", "tags": ["sito-daliamae"]}
    token = base64.b64encode(("daliamae:" + Config.MAILCHIMP_API_KEY).encode()).decode()
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), method="PUT",
                                 headers={"Authorization": "Basic " + token, "Content-Type": "application/json",
                                          "User-Agent": "daliamae-site/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return 200 <= r.status < 300, "inviato a Mailchimp", ""
    except urllib.error.HTTPError as e:
        body = e.read()[:400].decode("utf-8", "ignore")
        log.error("Mailchimp ha rifiutato l'iscrizione (%s): %s", e.code, body)
        try:
            detail = json.loads(body).get("title", "") or body
        except Exception:
            detail = body
        return False, "errore Mailchimp", detail[:200]
    except Exception as e:
        log.exception("Invio a Mailchimp non riuscito")
        return False, "errore Mailchimp", str(e)[:200]
