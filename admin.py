"""Pannello di controllo (/admin): SEO delle pagine, frasi chiave AEO, blog, video, eventi, richieste."""
import hmac
import re
import secrets
import unicodedata
from datetime import date, datetime
from functools import wraps

from flask import (Blueprint, abort, flash, redirect, render_template, request, session, url_for)

from config import Config
from models import AeoPhrase, Event, Lead, PageSEO, Post, Setting, Video, db
import seo

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ----------------------------------------------------------------------------- definizione dei moduli
F = lambda name, label, kind="text", **kw: dict(name=name, label=label, kind=kind, **kw)

GROUP_CHOICES = [("", "(nessuna scheda)"), ("op", "L'operatrice"), ("pr", "Le pratiche"), ("cf", "Come funziona")]

ENTITIES = {
    "blog": dict(
        model=Post, title="Articoli del blog", one="articolo", order=lambda: [Post.published_at.desc(), Post.id.desc()],
        cols=[("title", "Titolo"), ("published_at", "Data"), ("published", "Pubblicato")],
        fields=[
            F("title", "Titolo (H1)", required=True, maxlength=250),
            F("slug", "Indirizzo (URL)", help="Lascialo vuoto: lo creo dal titolo. Diventa /blog/…", maxlength=160),
            F("category", "Categoria", maxlength=80),
            F("published_at", "Data di pubblicazione", "date"),
            F("reading_min", "Minuti di lettura", "int"),
            F("excerpt", "Riassunto per l'elenco", "textarea", required=True, rows=3, help="2–3 frasi."),
            F("lead", "Frase di apertura sotto il titolo", "textarea", rows=2),
            F("body_html", "Testo dell'articolo", "html", rows=24,
              help="HTML semplice: <h2> per le sezioni, <p> per i paragrafi, <ol>/<li> per gli elenchi, <blockquote> per le citazioni. "
                   "Metti la risposta diretta alla domanda principale nel primo paragrafo (AEO)."),
            F("cover", "Immagine di copertina", help="Percorso di un file in static/ (es. img/metempsicosi.svg) oppure https://…", maxlength=300),
            F("cover_alt", "Descrizione dell'immagine (alt)", maxlength=300, help="Descrivi cosa si vede, con parole chiave naturali."),
            F("cover_caption", "Didascalia", "textarea", rows=2),
            F("meta_title", "Title per Google", maxlength=200, counter=60, help="Circa 50–60 caratteri, con la parola chiave principale."),
            F("meta_description", "Meta description", "textarea", rows=2, counter=155, help="Circa 120–155 caratteri."),
            F("keywords", "Parole chiave dell'articolo", help="Separate da virgola.", maxlength=500),
            F("published", "Pubblicato", "bool"),
            F("is_sample", "Mostra l'etichetta «Articolo di esempio»", "bool"),
        ]),
    "video": dict(
        model=Video, title="Video social", one="video", order=lambda: [Video.sort, Video.id],
        cols=[("title", "Titolo"), ("file", "File"), ("published", "Pubblicato")],
        fields=[
            F("title", "Titolo", required=True, maxlength=250),
            F("description", "Descrizione (testo letto da Google e dalle AI)", "textarea", rows=3),
            F("file", "File video", required=True, help="Percorso in static/ (es. video/stai-respirando.mp4) oppure link https:// diretto a un .mp4.", maxlength=300),
            F("poster", "Immagine di copertina", help="Es. video/stai-respirando.jpg", maxlength=300),
            F("upload_date", "Data di caricamento", "date"),
            F("sort", "Posizione (numero più basso = prima)", "int"),
            F("published", "Pubblicato", "bool"),
        ]),
    "eventi": dict(
        model=Event, title="Eventi", one="evento", order=lambda: [Event.starts_at.desc()],
        cols=[("title", "Titolo"), ("starts_at", "Data e ora"), ("published", "Pubblicato")],
        fields=[
            F("title", "Titolo", required=True, maxlength=250),
            F("starts_at", "Data e ora", "datetime", required=True),
            F("place", "Luogo", maxlength=250, help="Lascia vuoto se è online."),
            F("online", "Evento online", "bool"),
            F("seats", "Posti disponibili", "int"),
            F("description", "Descrizione", "textarea", rows=4),
            F("published", "Pubblicato", "bool"),
        ]),
    "aeo": dict(
        model=AeoPhrase, title="Frasi chiave AEO", one="frase chiave", order=lambda: [AeoPhrase.sort, AeoPhrase.id],
        cols=[("question", "Domanda"), ("words", "Parole"), ("pages_txt", "Pagine"), ("published", "Pubblicata")],
        fields=[
            F("question", "Domanda (come la scriverebbe una persona)", required=True, maxlength=300,
              help="Es. «Che cos'è l'oroscopo evolutivo?»"),
            F("answer", "Risposta diretta", "textarea", required=True, rows=6, words=True,
              help="Prima frase = risposta completa e citabile. In tutto 40–60 parole, tono semplice, senza promesse sanitarie."),
            F("group", "Scheda nella pagina Domande frequenti", "select", choices=GROUP_CHOICES),
            F("page_slugs", "Dove compare", "pages", help="Scegli le pagine che mostrano la domanda. Il markup FAQ per Google segue ciò che è visibile."),
            F("sort", "Posizione (numero più basso = prima)", "int"),
            F("published", "Pubblicata", "bool"),
        ]),
    "pagine": dict(
        model=PageSEO, title="SEO delle pagine", one="pagina", order=lambda: [PageSEO.id], no_create=True, no_delete=True,
        cols=[("label", "Pagina"), ("title", "Title"), ("seo_status", "Stato")],
        fields=[
            F("title", "Title (titolo che appare su Google)", maxlength=200, counter=60,
              help="Circa 50–60 caratteri. Parola chiave principale all'inizio, nome del brand alla fine."),
            F("meta_description", "Meta description", "textarea", rows=3, counter=155,
              help="Circa 120–155 caratteri: promessa chiara + parola chiave + invito all'azione."),
            F("keywords", "Parole chiave della pagina", help="Separate da virgola; 3–6 bastano.", maxlength=500),
        ]),
}

IDEAS = [
    "Che cosa sono i Nodi Lunari nell'astrologia evolutiva?",
    "Come si legge un tema natale?",
    "Come si fa una meditazione guidata a casa?",
    "Qual è la differenza tra meditazione guidata e mindfulness?",
    "Come funziona una meditazione di gruppo e cosa serve portare?",
    "Come si svolge una seduta di massaggio psicosomatico?",
    "Quanto dura un percorso di crescita personale?",
    "Cosa significa archetipo in astrologia?",
    "Come scegliere un'operatrice olistica?",
    "L'oroscopo evolutivo si può fare online?",
]


# ----------------------------------------------------------------------------- utilità
def slugify(text):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:140] or "articolo"


def all_page_slugs():
    return [(p.slug, p.label) for p in PageSEO.query.order_by(PageSEO.id).all()]


def parse_value(f, form):
    k, name = f["kind"], f["name"]
    if k == "bool":
        return form.get(name) == "1"
    if k == "pages":
        return ",".join(form.getlist(name))
    raw = (form.get(name) or "").strip()
    if k == "int":
        return int(raw) if raw.lstrip("-").isdigit() else None
    if k == "date":
        return date.fromisoformat(raw) if raw else None
    if k == "datetime":
        return datetime.fromisoformat(raw) if raw else None
    return raw


def get_val(obj, f):
    v = getattr(obj, f["name"], None) if obj is not None else None
    if f["kind"] == "datetime" and v:
        return v.strftime("%Y-%m-%dT%H:%M")
    if f["kind"] == "date" and v:
        return v.isoformat()
    return "" if v is None else v


def seo_status(p):
    msgs = []
    t, d = len(p.title or ""), len(p.meta_description or "")
    if not t:
        msgs.append("manca il title")
    elif t > 65:
        msgs.append("title lungo")
    elif t < 30:
        msgs.append("title corto")
    if not d:
        msgs.append("manca la description")
    elif d > 160:
        msgs.append("description lunga")
    elif d < 70:
        msgs.append("description corta")
    if not (p.keywords or "").strip():
        msgs.append("senza parole chiave")
    return "ok" if not msgs else ", ".join(msgs)


def cell(obj, name):
    if name == "pages_txt":
        return ", ".join(obj.pages) or "—"
    if name == "seo_status":
        return seo_status(obj)
    v = getattr(obj, name, "")
    if isinstance(v, bool):
        return "sì" if v else "no"
    if isinstance(v, datetime):
        return v.strftime("%d/%m/%Y %H:%M")
    if isinstance(v, date):
        return v.strftime("%d/%m/%Y")
    return v if v is not None else ""


def keywords_list():
    row = Setting.query.filter_by(key="keywords").first()
    text = row.value if row and row.value else "\n".join(seo.CORE_KEYWORDS)
    return [k.strip() for k in text.splitlines() if k.strip()]


# ----------------------------------------------------------------------------- accesso
@admin_bp.before_request
def require_login():
    if request.endpoint in ("admin.login",):
        return None
    if not session.get("admin"):
        return redirect(url_for("admin.login"))
    return None


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    from app import too_many
    if not Config.ADMIN_PASSWORD:
        return render_template("admin/login.html", disabled=True, error=None)
    error = None
    if request.method == "POST":
        if too_many("login:" + (request.remote_addr or "?"), limit=8):
            error = "Troppi tentativi: riprova tra qualche minuto."
        else:
            u_ok = hmac.compare_digest(request.form.get("username", "").encode(), Config.ADMIN_USERNAME.encode())
            p_ok = hmac.compare_digest(request.form.get("password", "").encode(), Config.ADMIN_PASSWORD.encode())
            if u_ok and p_ok:
                session.clear()
                session["admin"] = True
                session["csrf"] = secrets.token_urlsafe(24)
                return redirect(url_for("admin.dashboard"))
            error = "Nome utente o password non corretti."
    return render_template("admin/login.html", disabled=False, error=error)


@admin_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


# ----------------------------------------------------------------------------- cruscotto
@admin_bp.route("/")
def dashboard():
    pages = PageSEO.query.order_by(PageSEO.id).all()
    phrases = AeoPhrase.query.order_by(AeoPhrase.sort, AeoPhrase.id).all()
    live = [p for p in phrases if p.published]
    covered = set(s for p in live for s in p.pages)
    no_faq = [p for p in pages if p.slug not in covered and (p.slug.startswith("percorsi/") or p.slug in ("domande-frequenti", "la-visione"))]
    off_words = [p for p in live if not (30 <= p.words <= 75)]
    seo_issues = [(p, seo_status(p)) for p in pages if seo_status(p) != "ok"]
    # uso delle parole chiave nei testi del sito
    blob = " ".join([(p.title or "") + " " + (p.meta_description or "") for p in pages] +
                    [a.question + " " + a.answer for a in live] +
                    [(x.title or "") + " " + (x.excerpt or "") + " " + (x.body_html or "") for x in Post.query.filter_by(published=True).all()]).lower()
    usage = [(k, blob.count(k.lower())) for k in keywords_list()]
    stats = dict(
        leads=Lead.query.filter_by(handled=False).count(), posts=Post.query.filter_by(published=True).count(),
        videos=Video.query.filter_by(published=True).count(), aeo=len(live), events=Event.query.filter_by(published=True).count())
    return render_template("admin/dashboard.html", stats=stats, seo_issues=seo_issues, no_faq=no_faq,
                           off_words=off_words, usage=usage, npages=len(pages))


# ----------------------------------------------------------------------------- parole chiave
@admin_bp.route("/parole-chiave", methods=["GET", "POST"])
def keywords():
    row = Setting.query.filter_by(key="keywords").first()
    if request.method == "POST":
        text = "\n".join(k.strip() for k in request.form.get("keywords", "").splitlines() if k.strip())
        if row is None:
            row = Setting(key="keywords", value=text)
            db.session.add(row)
        else:
            row.value = text
        db.session.commit()
        flash("Parole chiave salvate.", "ok")
        return redirect(url_for("admin.keywords"))
    return render_template("admin/keywords.html", text="\n".join(keywords_list()))


# ----------------------------------------------------------------------------- richieste dal modulo contatti
@admin_bp.route("/richieste")
def leads():
    rows = Lead.query.order_by(Lead.created_at.desc()).all()
    return render_template("admin/leads.html", rows=rows)


@admin_bp.route("/richieste/<int:lid>/gestita", methods=["POST"])
def lead_toggle(lid):
    row = db.session.get(Lead, lid) or abort(404)
    row.handled = not row.handled
    db.session.commit()
    return redirect(url_for("admin.leads"))


@admin_bp.route("/richieste/<int:lid>/elimina", methods=["POST"])
def lead_delete(lid):
    row = db.session.get(Lead, lid) or abort(404)
    db.session.delete(row)
    db.session.commit()
    flash("Richiesta eliminata.", "ok")
    return redirect(url_for("admin.leads"))


# ----------------------------------------------------------------------------- elenco / modulo / elimina (generici)
def _ent(key):
    e = ENTITIES.get(key)
    if not e:
        abort(404)
    return e


@admin_bp.route("/<key>")
def listing(key):
    e = _ent(key)
    rows = e["model"].query.order_by(*e["order"]()).all()
    ideas = []
    if key == "aeo":
        have = {r.question.strip().lower() for r in rows}
        ideas = [i for i in IDEAS if i.lower() not in have]
    return render_template("admin/list.html", key=key, e=e, rows=rows, cell=cell, ideas=ideas)


@admin_bp.route("/<key>/nuovo", methods=["GET", "POST"])
def create(key):
    e = _ent(key)
    if e.get("no_create"):
        abort(404)
    return _form(key, e, None)


@admin_bp.route("/<key>/<int:oid>", methods=["GET", "POST"])
def edit(key, oid):
    e = _ent(key)
    obj = db.session.get(e["model"], oid) or abort(404)
    return _form(key, e, obj)


def _form(key, e, obj):
    fields = e["fields"]
    values = {}
    if request.method == "POST":
        errors = []
        parsed = {}
        for f in fields:
            try:
                parsed[f["name"]] = parse_value(f, request.form)
            except ValueError:
                errors.append("Valore non valido in «%s»." % f["label"])
                continue
            if f.get("required") and parsed[f["name"]] in ("", None):
                errors.append("«%s» è obbligatorio." % f["label"])
        if not errors:
            new = obj is None
            if new:
                obj = e["model"]()
            for name, v in parsed.items():
                setattr(obj, name, v)
            if key == "blog":
                base = slugify(parsed.get("slug") or parsed["title"])
                slug, n = base, 2
                while True:
                    clash = Post.query.filter_by(slug=slug).first()
                    if clash is None or (not new and clash.id == obj.id):
                        break
                    slug, n = "%s-%d" % (base, n), n + 1
                obj.slug = slug
                if not obj.published_at:
                    obj.published_at = date.today()
            if new:
                db.session.add(obj)
            db.session.commit()
            flash("Salvato.", "ok")
            return redirect(url_for("admin.listing", key=key))
        for msg in errors:
            flash(msg, "err")
        values = {f["name"]: (request.form.getlist(f["name"]) if f["kind"] == "pages" else request.form.get(f["name"], "")) for f in fields}
        values["__post"] = True
    else:
        for f in fields:
            values[f["name"]] = get_val(obj, f)
        if key == "aeo" and obj is None and request.args.get("q"):
            values["question"] = request.args["q"]
        if obj is None:
            for f in fields:
                if f["kind"] == "bool" and f["name"] == "published":
                    values["published"] = True
                if f["kind"] == "date" and not values.get(f["name"]):
                    values[f["name"]] = date.today().isoformat()
                if f["name"] == "sort" and values.get("sort", "") == "":
                    values["sort"] = 50
                if f["name"] == "reading_min":
                    values["reading_min"] = 5
    page_choices = all_page_slugs() if key == "aeo" else []
    selected = values.get("page_slugs", "")
    if isinstance(selected, str):
        selected = [s for s in selected.split(",") if s]
    return render_template("admin/form.html", key=key, e=e, obj=obj, values=values, fields=fields,
                           page_choices=page_choices, selected=selected)


@admin_bp.route("/<key>/<int:oid>/elimina", methods=["POST"])
def delete(key, oid):
    e = _ent(key)
    if e.get("no_delete"):
        abort(404)
    obj = db.session.get(e["model"], oid) or abort(404)
    db.session.delete(obj)
    db.session.commit()
    flash("Eliminato.", "ok")
    return redirect(url_for("admin.listing", key=key))
