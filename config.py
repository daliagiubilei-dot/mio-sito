"""Configurazione: tutto ciò che cambia tra il computer e Railway arriva da variabili d'ambiente."""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Su Railway queste variabili esistono sempre: le usiamo per capire che siamo "in produzione".
IS_PROD = bool(os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("RAILWAY_PROJECT_ID")
               or os.environ.get("PRODUCTION"))


def _database_url():
    url = os.environ.get("DATABASE_URL", "").strip()
    # Railway/Heroku possono fornire "postgres://", SQLAlchemy vuole "postgresql://"
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    if not url:
        if IS_PROD:
            raise RuntimeError("DATABASE_URL mancante: collega il database PostgreSQL al servizio su Railway.")
        url = "sqlite:///" + os.path.join(BASE_DIR, "local.db")   # solo per provare in locale
    return url


def _secret_key():
    key = os.environ.get("SECRET_KEY", "").strip()
    if not key:
        if IS_PROD:
            raise RuntimeError("SECRET_KEY mancante: aggiungila alle variabili del servizio su Railway.")
        key = "chiave-solo-per-sviluppo-locale"
    return key


class Config:
    SECRET_KEY = _secret_key()
    SQLALCHEMY_DATABASE_URI = _database_url()
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = IS_PROD
    SEND_FILE_MAX_AGE_DEFAULT = 60 * 60 * 24 * 7      # 7 giorni di cache per immagini e video
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024               # i moduli non devono superare 1 MB

    # Pannello di controllo
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "dalia")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")

    # Indirizzo pubblico (es. https://www.daliamae.it). Se vuoto si usa quello della richiesta.
    SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")

    # Email di avviso quando arriva una richiesta dal modulo contatti (facoltativa)
    SMTP_HOST = os.environ.get("SMTP_HOST", "")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USER = os.environ.get("SMTP_USER", "")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
    MAIL_TO = os.environ.get("MAIL_TO", "")


# Dati del brand (compaiono nel sito e nei dati strutturati per Google)
SITE = {
    "name": "Daliamae",
    "owner": "Dalia Giubilei",
    "role": "Operatrice olistica",
    "phone": "331 758 4001",
    "phone_raw": "3317584001",
    "phone_intl": "+393317584001",
    "vat": "18680741008",
    "instagram": "https://www.instagram.com/daliamae_/",
    "tiktok": "https://www.tiktok.com/@daliamae77",
    # Facebook: compare nel sito solo se imposti FACEBOOK_URL
    "facebook": os.environ.get("FACEBOOK_URL", "").strip(),
}
