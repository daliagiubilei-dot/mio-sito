"""Invio dell'email di avviso quando qualcuno compila il modulo Contatti.

Su Railway i piani Free, Trial e Hobby bloccano la posta via SMTP: per questo il metodo principale è un servizio
di invio con interfaccia web (HTTPS), qui Resend. L'SMTP resta disponibile solo come alternativa (piano Pro).
"""
import json
import logging
import re
import smtplib
import urllib.error
import urllib.request
from email.message import EmailMessage

from config import Config

log = logging.getLogger("daliamae.mail")
_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_configured():
    return bool(Config.MAIL_TO and (Config.RESEND_API_KEY or Config.SMTP_HOST))


def _recipients():
    return [a.strip() for a in Config.MAIL_TO.split(",") if a.strip()]


def _send_resend(subject, body, reply_to):
    payload = {"from": Config.MAIL_FROM, "to": _recipients(), "subject": subject, "text": body}
    if reply_to:
        payload["reply_to"] = reply_to
    req = urllib.request.Request(
        "https://api.resend.com/emails", data=json.dumps(payload).encode("utf-8"), method="POST",
        headers={"Authorization": "Bearer " + Config.RESEND_API_KEY, "Content-Type": "application/json",
                 "User-Agent": "daliamae-site/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            if 200 <= r.status < 300:
                log.info("Email inviata con Resend a %s", ", ".join(_recipients()))
                return True, "Email inviata a %s." % ", ".join(_recipients())
            return False, "Resend ha risposto con il codice %s." % r.status
    except urllib.error.HTTPError as e:
        detail = e.read()[:300].decode("utf-8", "replace")
        log.error("Resend ha rifiutato l'email (%s): %s", e.code, detail)
        return False, "Resend ha rifiutato l'email (codice %s): %s" % (e.code, detail)
    except Exception as e:
        log.exception("Invio con Resend non riuscito")
        return False, "Il sito non è riuscito a contattare Resend: %s" % e


def _send_smtp(subject, body, reply_to):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = Config.SMTP_USER or _recipients()[0]
        msg["To"] = ", ".join(_recipients())
        if reply_to:
            msg["Reply-To"] = reply_to
        msg.set_content(body)
        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT, timeout=10) as s:
            s.starttls()
            if Config.SMTP_USER:
                s.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            s.send_message(msg)
        log.info("Email inviata via SMTP a %s", ", ".join(_recipients()))
        return True, "Email inviata a %s." % ", ".join(_recipients())
    except Exception as e:
        log.exception("Invio SMTP non riuscito")
        return False, "Invio SMTP non riuscito: %s" % e


def status():
    """Descrizione leggibile della configurazione (senza mostrare la chiave)."""
    missing = [n for n, v in (("MAIL_TO", Config.MAIL_TO), ("RESEND_API_KEY", Config.RESEND_API_KEY or Config.SMTP_HOST)) if not v]
    if missing:
        return False, "Email di avviso NON configurata: mancano le variabili " + ", ".join(missing) + "."
    method = "Resend" if Config.RESEND_API_KEY else "SMTP"
    return True, "Email di avviso configurata con %s: mittente %s, destinatari %s." % (
        method, Config.MAIL_FROM if Config.RESEND_API_KEY else (Config.SMTP_USER or "-"), ", ".join(_recipients()))


def _send(subject, body, reply_to=None):
    if not is_configured():
        return False, status()[1]
    if Config.RESEND_API_KEY:
        return _send_resend(subject, body, reply_to)
    return _send_smtp(subject, body, reply_to)


def send_test_email():
    """Email di prova dal pannello: ritorna (riuscito, spiegazione)."""
    return _send("Prova email dal sito Daliamae",
                 "Questa è un'email di prova inviata dal pannello di controllo del sito Daliamae.\n"
                 "Se la leggi, gli avvisi del modulo Contatti funzionano.")


def send_lead_email(lead):
    """Spedisce a Dalia i dati di una nuova richiesta. Ritorna (riuscito, spiegazione)."""
    subject = "Nuova richiesta dal sito: %s" % lead.name
    body = "Nome: %s\nRecapito: %s\nInteresse: %s\n\nMessaggio:\n%s\n\n— Richiesta ricevuta dal sito Daliamae." % (
        lead.name, lead.contact, lead.interest or "-", lead.message or "(nessun messaggio)")
    reply_to = lead.contact if _EMAIL.match(lead.contact or "") else None
    return _send(subject, body, reply_to)
