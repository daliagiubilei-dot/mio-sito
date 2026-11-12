"""Controllo dei recapiti lasciati nei moduli del sito (email o telefono).

Per le email non basta il formato: si verifica anche che il dominio esista e possa ricevere posta
(record MX, oppure in mancanza un indirizzo del dominio). Se il controllo DNS non risponde per un problema
di rete, l'indirizzo viene accettato: meglio una richiesta in più che perdere una persona vera.
"""
import logging
import re
import socket

log = logging.getLogger("daliamae.validators")

EMAIL_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@([A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
                      r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*\.[A-Za-z]{2,})$")
PHONE_RE = re.compile(r"^\+?\d{8,15}$")

# Errori di battitura frequenti nei domini più usati.
TYPOS = {
    "gmial.com": "gmail.com", "gmai.com": "gmail.com", "gmal.com": "gmail.com",
    "gamil.com": "gmail.com", "gmail.co": "gmail.com", "gmail.con": "gmail.com", "gnail.com": "gmail.com",
    "hotmial.com": "hotmail.com", "hotmail.con": "hotmail.com", "hotmal.it": "hotmail.it",
    "libero.com": "libero.it", "libro.it": "libero.it", "yaho.it": "yahoo.it", "yahoo.con": "yahoo.com",
    "virgilo.it": "virgilio.it", "outlok.it": "outlook.it", "outlok.com": "outlook.com", "iclod.com": "icloud.com",
}

# Domini molto diffusi: sempre validi, senza interrogare il DNS.
KNOWN = {"gmail.com", "googlemail.com", "libero.it", "hotmail.com", "hotmail.it", "outlook.com", "outlook.it",
         "live.com", "live.it", "yahoo.com", "yahoo.it", "icloud.com", "me.com", "virgilio.it", "tiscali.it",
         "alice.it", "tim.it", "fastwebnet.it", "email.it", "pec.it", "msn.com", "aol.com", "proton.me",
         "protonmail.com", "inwind.it", "tin.it", "daliamae.com", "daliamae.it"}

_cache = {}


def _domain_ok(domain):
    """True se il dominio può ricevere posta, False se non esiste, None se il controllo non è riuscito."""
    domain = domain.lower()
    if domain in _cache:
        return _cache[domain]
    result = None
    try:
        import dns.resolver
        import dns.exception
        r = dns.resolver.Resolver()
        r.lifetime = 4
        try:
            result = bool(r.resolve(domain, "MX"))
        except (dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            try:                                   # nessun MX: va bene anche un indirizzo del dominio
                result = bool(r.resolve(domain, "A"))
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                result = False
        except dns.resolver.NXDOMAIN:
            result = False
        except dns.exception.DNSException:
            result = None
    except ImportError:                            # dnspython non installato: controllo semplice
        try:
            socket.setdefaulttimeout(4)
            socket.getaddrinfo(domain, None)
            result = True
        except socket.gaierror as e:
            result = False if e.errno in (socket.EAI_NONAME, getattr(socket, "EAI_NODATA", -5)) else None
            if result is False:                    # il DNS del server funziona? se no, non bloccare nessuno
                try:
                    socket.getaddrinfo("gmail.com", None)
                except Exception:
                    result = None
        except Exception:
            result = None
    if result is not None:
        _cache[domain] = result
    return result


def check_email(value):
    """Ritorna (email ripulita, messaggio di errore o None)."""
    email = (value or "").strip()
    m = EMAIL_RE.match(email)
    if not m:
        return email, "L'indirizzo email non sembra corretto: controlla che ci siano la @ e il dominio (es. nome@gmail.com)."
    domain = m.group(1).lower()
    if domain in TYPOS:
        return email, "Forse volevi scrivere %s@%s? Controlla l'indirizzo email." % (email.split("@")[0], TYPOS[domain])
    ok = True if domain in KNOWN else _domain_ok(domain)
    if ok is False:
        return email, "Il dominio «%s» non esiste o non riceve email: controlla l'indirizzo." % domain
    if ok is None:
        log.warning("Controllo DNS non riuscito per %s: indirizzo accettato", domain)
    return email.lower(), None


def check_contact(value):
    """Recapito del modulo Contatti: email valida oppure numero di telefono. Ritorna (recapito, errore o None)."""
    v = (value or "").strip()
    if "@" in v:
        return check_email(v)
    digits = re.sub(r"[\s.\-/()]", "", v)
    if digits.startswith("00"):
        digits = "+" + digits[2:]
    if PHONE_RE.match(digits):
        return v, None
    return v, "Scrivi un'email valida (es. nome@gmail.com) o un numero di telefono completo, così posso ricontattarti."
