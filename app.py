"""Sito Daliamae – applicazione Flask.

Avvio in locale:   python app.py
Avvio su Railway:  gunicorn app:app   (vedi Procfile)
"""
import hmac
import json
import logging
import os
import secrets
import threading
import time
from collections import defaultdict
from datetime import datetime

from flask import (Flask, abort, flash, jsonify, make_response, redirect, render_template, request,
                   session, url_for)
from markupsafe import Markup
from werkzeug.middleware.proxy_fix import ProxyFix

import mailer
import newsletter
import seo
from config import Config, SITE
from content import FAQ_GROUPS, INTERESTS, SERVICES, SIGNS
from models import AeoPhrase, Event, Lead, Post, PageSEO, Setting, Subscriber, Video, db, static_or_url
from seed_data import seed_if_empty

log = logging.getLogger("daliamae")

MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
        "settembre", "ottobre", "novembre", "dicembre"]

_hits = defaultdict(list)       # limitatore semplice per IP (moduli e login)


def too_many(key, limit=6, window=600):
    now = time.time()
    _hits[key] = [t for t in _hits[key] if now - t < window]
    if len(_hits[key]) >= limit:
        return True
    _hits[key].append(now)
    return False


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    db.init_app(app)

    from admin import admin_bp
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        seed_if_empty()

    # ------------------------------------------------------------------ utilità per i template
    @app.template_filter("tojson_ld")
    def tojson_ld(value):
        return Markup(json.dumps(value, ensure_ascii=False).replace("<", "\\u003c"))

    @app.template_filter("it_month")
    def it_month(d):
        return "%s %d" % (MESI[d.month - 1].capitalize(), d.year) if d else ""

    @app.template_filter("it_datetime")
    def it_datetime(d):
        return "%d %s %d, ore %02d:%02d" % (d.day, MESI[d.month - 1], d.year, d.hour, d.minute) if d else ""

    def csrf_token():
        if "csrf" not in session:
            session["csrf"] = secrets.token_urlsafe(24)
        return session["csrf"]

    def faqs_for(slug):
        rows = AeoPhrase.query.filter_by(published=True).order_by(AeoPhrase.sort, AeoPhrase.id).all()
        return [r for r in rows if slug in r.pages]

    def asset(path):
        """Indirizzo di un file statico con un numero di versione: quando il file cambia, i browser lo ricaricano
        subito invece di tenere in memoria per giorni la versione vecchia."""
        url = url_for("static", filename=path)
        try:
            return "%s?v=%d" % (url, os.path.getmtime(os.path.join(app.static_folder, path)))
        except OSError:
            return url

    @app.context_processor
    def inject():
        return {"site": SITE, "csrf_token": csrf_token, "asset": asset, "nl_consent": newsletter.CONSENT_TEXT,
                "aeo_first": lambda slug: (faqs_for(slug) or [None])[0]}

    # ------------------------------------------------------------------ sicurezza di base
    @app.before_request
    def check_csrf():
        if request.method == "POST":
            sent = request.form.get("csrf", "")
            if not sent or not hmac.compare_digest(sent, session.get("csrf", "")):
                abort(400)

    @app.after_request
    def headers(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        resp.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        if request.path.startswith("/admin"):
            resp.headers["Cache-Control"] = "no-store"
            resp.headers["X-Robots-Tag"] = "noindex, nofollow"
        return resp

    # ------------------------------------------------------------------ SEO: metadati e dati strutturati
    def base_url():
        return Config.SITE_URL or request.url_root.rstrip("/")

    def keywords_list():
        row = Setting.query.filter_by(key="keywords").first()
        text = row.value if row and row.value else "\n".join(seo.CORE_KEYWORDS)
        return [k.strip() for k in text.splitlines() if k.strip()]

    def meta_for(slug, **over):
        row = PageSEO.query.filter_by(slug=slug).first()
        d = seo.PAGE_DEFAULTS.get(slug)
        title = (row.title if row and row.title else (d[1] if d else SITE["name"]))
        desc = (row.meta_description if row and row.meta_description else (d[2] if d else ""))
        kw = (row.keywords if row and row.keywords else (d[3] if d else ""))
        path = "/" if slug == "home" else "/" + slug
        meta = {"title": title, "description": desc, "keywords": kw, "robots": "index, follow, max-snippet:-1, max-image-preview:large",
                "canonical": base_url() + path, "og_type": "website",
                "image": base_url() + url_for("static", filename="img/og-default.jpg")}
        meta.update(over)
        return meta

    def render(template, slug, ld_extra=(), meta_over=None, **ctx):
        meta = meta_for(slug, **(meta_over or {}))
        ld = [seo.ld_organization(SITE, base_url(), keywords_list())]
        if slug == "home":
            ld.append(seo.ld_website(SITE, base_url()))
        else:
            ld.append(seo.ld_breadcrumb(base_url(), [(ctx.pop("crumb", None) or meta_for(slug)["title"].split("|")[0].strip(), meta["canonical"])]))
        ld.extend(ld_extra)
        return render_template(template, meta=meta, ld=ld, **ctx)

    # ------------------------------------------------------------------ pagine
    @app.route("/")
    def home():
        return render("home.html", "home")

    @app.route("/la-visione")
    def visione():
        return render("visione.html", "la-visione", crumb="La Visione")

    @app.route("/chi-sono")
    def chi_sono():
        return render("chi_sono.html", "chi-sono", crumb="Chi sono")

    @app.route("/percorsi")
    def percorsi():
        return render("percorsi.html", "percorsi", crumb="Pratiche e Percorsi")

    @app.route("/percorsi/<slug>")
    def service(slug):
        svc = SERVICES.get(slug)
        if not svc:
            abort(404)
        key = "percorsi/" + slug
        faqs = faqs_for(key)
        meta = meta_for(key)
        ld = [seo.ld_service(svc, meta["canonical"], base_url())]
        if faqs:
            ld.append(seo.ld_faq(faqs))
        others = [dict(slug=s, name=v["name"]) for s, v in SERVICES.items() if s != slug]
        return render("service.html", key, ld_extra=ld, crumb=svc["name"], svc=svc, faqs=faqs, others=others,
                      faq_title="Domande su " + svc["name"].lower())

    @app.route("/archetipi-astrologici")
    def archetipi():
        signs = [dict(symbol=s[0], name=s[1], element=s[2], archetype=s[3], text=s[4]) for s in SIGNS]
        return render("archetipi.html", "archetipi-astrologici", crumb="Archetipi astrologici", signs=signs)

    @app.route("/eventi")
    def eventi():
        now = datetime.utcnow()
        evs = [e for e in Event.query.filter_by(published=True).order_by(Event.starts_at).all() if e.starts_at >= now]
        meta = meta_for("eventi")
        ld = [seo.ld_event(e, meta["canonical"], base_url()) for e in evs]
        return render("eventi.html", "eventi", ld_extra=ld, crumb="Eventi", events=evs)

    @app.route("/blog")
    def blog():
        posts = Post.query.filter_by(published=True).order_by(Post.published_at.desc(), Post.id.desc()).all()
        return render("blog.html", "blog", crumb="Blog", posts=posts)

    @app.route("/blog/<slug>")
    def post(slug):
        p = Post.query.filter_by(slug=slug, published=True).first()
        if not p:
            abort(404)
        url = base_url() + "/blog/" + p.slug
        image = (base_url() + p.cover_url) if p.cover and p.cover_url.startswith("/") else (p.cover_url or None)
        over = {"title": p.meta_title or (p.title + " – Daliamae"),
                "description": p.meta_description or p.excerpt[:155],
                "keywords": p.keywords, "canonical": url, "og_type": "article"}
        if image:
            over["image"] = image
        meta = meta_for("blog", **over)
        ld = [seo.ld_article(p, url, image, base_url()),
              seo.ld_breadcrumb(base_url(), [("Blog", base_url() + "/blog"), (p.title, url)])]
        return render_template("blog_post.html", meta=meta, ld=[seo.ld_organization(SITE, base_url(), keywords_list())] + ld, post=p)

    @app.route("/video-social")
    def video_social():
        vids = Video.query.filter_by(published=True).order_by(Video.sort, Video.id).all()
        ld = []
        for v in vids:
            f = static_or_url(v.file)
            f = base_url() + f if f.startswith("/") else f
            pu = static_or_url(v.poster)
            pu = base_url() + pu if pu.startswith("/") else pu
            ld.append(seo.ld_video(v, f, pu, base_url() + "/video-social"))
        return render("video_social.html", "video-social", ld_extra=ld, crumb="Video Social", videos=vids)

    @app.route("/domande-frequenti")
    def domande():
        faqs = faqs_for("domande-frequenti")
        groups = []
        for key, label in FAQ_GROUPS:
            items = [f for f in faqs if f.group == key]
            if items:
                groups.append({"key": key, "label": label, "faqs": items})
        rest = [f for f in faqs if f.group not in dict(FAQ_GROUPS)]
        if rest:
            groups.append({"key": "altro", "label": "Altre domande", "faqs": rest})
        return render("domande.html", "domande-frequenti", ld_extra=[seo.ld_faq(faqs)] if faqs else [],
                      crumb="Domande frequenti", groups=groups)

    @app.route("/contatti", methods=["GET", "POST"])
    def contatti():
        form, error = {}, None
        if request.method == "POST":
            form = request.form
            ip = request.remote_addr or "?"
            if form.get("website"):                      # campo trappola per i bot
                return redirect(url_for("contatti", inviato=1))
            if too_many("lead:" + ip, limit=5):
                error = "Hai inviato troppe richieste: riprova tra qualche minuto."
            elif not (form.get("nome", "").strip() and form.get("contatto", "").strip() and form.get("consenso")):
                error = "Compila nome e recapito e acconsenti al trattamento dei dati."
            else:
                lead = Lead(name=form["nome"].strip()[:120], contact=form["contatto"].strip()[:200],
                            interest=form.get("pratica", "")[:120], message=form.get("messaggio", "").strip()[:2000],
                            consent=True)
                db.session.add(lead)
                db.session.commit()
                notify(lead)
                return redirect(url_for("contatti", inviato=1))
        else:
            pr = request.args.get("pratica", "")
            if pr in INTERESTS:
                form = {"pratica": pr}
        return render("contatti.html", "contatti", crumb="Contatti", form=form, error=error,
                      sent=bool(request.args.get("inviato")), interests=INTERESTS)

    @app.route("/newsletter", methods=["POST"])
    def newsletter_signup():
        form = request.form
        back = request.referrer or url_for("home")
        if form.get("website"):                                   # campo trappola per i bot
            return redirect(url_for("newsletter_thanks"))
        email = (form.get("email") or "").strip().lower()[:200]
        if too_many("nl:" + (request.remote_addr or "?"), limit=5):
            flash("Troppi tentativi: riprova tra qualche minuto.", "err")
            return redirect(back)
        if not newsletter.EMAIL_RE.match(email) or not form.get("consenso"):
            flash("Inserisci un indirizzo email valido e accetta il consenso per iscriverti.", "err")
            return redirect(back)
        sub = Subscriber.query.filter_by(email=email).first()
        if sub is None:
            sub = Subscriber(email=email, source=(request.form.get("source") or "")[:200],
                             consent_version=newsletter.CONSENT_VERSION)
            db.session.add(sub)
        ok, status, err = newsletter.subscribe_mailchimp(email)
        sub.mailchimp_status, sub.mailchimp_error = status, err
        db.session.commit()
        session["nl_confirm"] = bool(ok)
        return redirect(url_for("newsletter_thanks"))

    @app.route("/newsletter/grazie")
    def newsletter_thanks():
        meta = {"title": "Iscrizione alla newsletter – Daliamae", "description": "Grazie per l'iscrizione.",
                "keywords": "", "robots": "noindex", "canonical": base_url() + "/newsletter/grazie",
                "og_type": "website", "image": base_url() + url_for("static", filename="img/og-default.jpg")}
        return render_template("newsletter_grazie.html", meta=meta, ld=[], confirm=session.pop("nl_confirm", False))

    def notify(lead):
        """Avvisa Dalia via email (solo se la posta è configurata). Parte in secondo piano: il sito non aspetta."""
        if not mailer.is_configured():
            return
        threading.Thread(target=mailer.send_lead_email, args=(lead,), daemon=True).start()

    # ------------------------------------------------------------------ file per motori di ricerca e AI
    @app.route("/robots.txt")
    def robots():
        txt = "User-agent: *\nAllow: /\nDisallow: /admin\n\nSitemap: %s/sitemap.xml\n" % base_url()
        return make_response(txt, 200, {"Content-Type": "text/plain; charset=utf-8"})

    @app.route("/sitemap.xml")
    def sitemap():
        urls = [("/", None)]
        for slug in ("la-visione", "chi-sono", "percorsi", "archetipi-astrologici", "eventi", "blog",
                     "video-social", "domande-frequenti", "contatti"):
            urls.append(("/" + slug, None))
        urls += [("/percorsi/" + s, None) for s in SERVICES]
        for p in Post.query.filter_by(published=True).all():
            urls.append(("/blog/" + p.slug, (p.updated_at or datetime.utcnow()).date().isoformat()))
        body = "".join("<url><loc>%s%s</loc>%s</url>" % (base_url(), u, "<lastmod>%s</lastmod>" % m if m else "") for u, m in urls)
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>' % body
        return make_response(xml, 200, {"Content-Type": "application/xml; charset=utf-8"})

    @app.route("/llms.txt")
    def llms():
        """Riassunto del sito per gli assistenti AI, costruito dalle frasi chiave AEO del pannello."""
        lines = ["# Daliamae – Dalia Giubilei, operatrice olistica", "",
                 "> Oroscopo evolutivo, meditazioni guidate, percorsi di crescita personale e massaggio psicosomatico. "
                 "Attività di benessere ai sensi della Legge 4/2013, non sanitaria.", "", "## Pagine principali"]
        for slug, svc in SERVICES.items():
            lines.append("- [%s](%s/percorsi/%s): %s" % (svc["name"], base_url(), slug, svc["intro"]))
        lines += ["- [Domande frequenti](%s/domande-frequenti)" % base_url(), "- [Blog](%s/blog)" % base_url(),
                  "- [Contatti](%s/contatti)" % base_url(), "", "## Domande e risposte"]
        for f in AeoPhrase.query.filter_by(published=True).order_by(AeoPhrase.sort, AeoPhrase.id).all():
            lines += ["", "**%s**" % f.question, f.answer]
        return make_response("\n".join(lines) + "\n", 200, {"Content-Type": "text/plain; charset=utf-8"})

    @app.route("/healthz")
    def healthz():
        return jsonify(status="ok")

    @app.errorhandler(404)
    def not_found(e):
        meta = {"title": "Pagina non trovata – Daliamae", "description": "La pagina che cerchi non esiste.",
                "keywords": "", "robots": "noindex", "canonical": base_url() + request.path, "og_type": "website",
                "image": base_url() + url_for("static", filename="img/og-default.jpg")}
        return render_template("404.html", meta=meta, ld=[]), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
