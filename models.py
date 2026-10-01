"""Tabelle del database (PostgreSQL su Railway, SQLite in locale)."""
from datetime import datetime, date

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def _now():
    return datetime.utcnow()


def static_or_url(path):
    """Un file nella cartella static (es. 'video/x.mp4') oppure un indirizzo completo (https://...)."""
    from flask import url_for
    if not path:
        return ""
    if path.startswith(("http://", "https://", "/")):
        return path
    return url_for("static", filename=path)


class Setting(db.Model):
    """Impostazioni modificabili dal pannello (es. elenco delle parole chiave)."""
    __tablename__ = "settings"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.Text, default="")


class PageSEO(db.Model):
    """Title, meta description e parole chiave di ogni pagina."""
    __tablename__ = "page_seo"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    label = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(200), default="")
    meta_description = db.Column(db.String(400), default="")
    keywords = db.Column(db.String(500), default="")
    updated_at = db.Column(db.DateTime, default=_now, onupdate=_now)


class AeoPhrase(db.Model):
    """Frasi chiave per l'AEO: domanda + risposta diretta, citabile da assistenti e motori di risposta."""
    __tablename__ = "aeo_phrases"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    group = db.Column(db.String(10), default="")            # op / pr / cf (schede della pagina Domande)
    page_slugs = db.Column(db.String(500), default="")      # pagine in cui compare, separate da virgola
    sort = db.Column(db.Integer, default=50)
    published = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=_now, onupdate=_now)

    @property
    def pages(self):
        return [p.strip() for p in (self.page_slugs or "").split(",") if p.strip()]

    @property
    def words(self):
        return len((self.answer or "").split())


class Post(db.Model):
    """Articoli del blog (uno al mese)."""
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(160), unique=True, nullable=False)
    title = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(80), default="")
    excerpt = db.Column(db.Text, default="")
    lead = db.Column(db.Text, default="")
    body_html = db.Column(db.Text, default="")
    cover = db.Column(db.String(300), default="")           # es. img/metempsicosi.svg
    cover_alt = db.Column(db.String(300), default="")
    cover_caption = db.Column(db.Text, default="")
    published_at = db.Column(db.Date, default=date.today)
    reading_min = db.Column(db.Integer, default=5)
    meta_title = db.Column(db.String(200), default="")
    meta_description = db.Column(db.String(400), default="")
    keywords = db.Column(db.String(500), default="")
    published = db.Column(db.Boolean, default=True)
    is_sample = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=_now)
    updated_at = db.Column(db.DateTime, default=_now, onupdate=_now)

    @property
    def cover_url(self):
        return static_or_url(self.cover)


class Video(db.Model):
    __tablename__ = "videos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, default="")
    file = db.Column(db.String(300), nullable=False)        # es. video/stai-respirando.mp4
    poster = db.Column(db.String(300), default="")
    upload_date = db.Column(db.Date, default=date.today)
    sort = db.Column(db.Integer, default=50)
    published = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=_now, onupdate=_now)

    @property
    def file_url(self):
        return static_or_url(self.file)

    @property
    def poster_url(self):
        return static_or_url(self.poster)


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, default="")
    starts_at = db.Column(db.DateTime, nullable=False)
    place = db.Column(db.String(250), default="")
    online = db.Column(db.Boolean, default=False)
    seats = db.Column(db.Integer)
    published = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=_now, onupdate=_now)


class Lead(db.Model):
    """Richieste arrivate dal modulo Contatti."""
    __tablename__ = "leads"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.String(200), nullable=False)
    interest = db.Column(db.String(120), default="")
    message = db.Column(db.Text, default="")
    consent = db.Column(db.Boolean, default=False)
    handled = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=_now)
