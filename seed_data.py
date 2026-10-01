"""Riempie il database al primo avvio con i contenuti del prototipo."""
import json
import os
from datetime import date, datetime

from models import db, PageSEO, AeoPhrase, Post, Video, Setting
from seo import PAGE_DEFAULTS, CORE_KEYWORDS

SEED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed")


def _read(name):
    with open(os.path.join(SEED_DIR, name), encoding="utf-8") as f:
        return f.read()


def seed_if_empty():
    try:
        if PageSEO.query.count() == 0:
            for slug, (label, title, desc, kw) in PAGE_DEFAULTS.items():
                db.session.add(PageSEO(slug=slug, label=label, title=title, meta_description=desc, keywords=kw))
        if Setting.query.filter_by(key="keywords").first() is None:
            db.session.add(Setting(key="keywords", value="\n".join(CORE_KEYWORDS)))
        if AeoPhrase.query.count() == 0:
            for item in json.loads(_read("aeo.json")):
                db.session.add(AeoPhrase(question=item["question"], answer=item["answer"], group=item["group"],
                                         page_slugs=",".join(item["pages"]), sort=item["sort"], published=True))
        if Post.query.count() == 0:
            db.session.add(Post(
                slug="metempsicosi", title="Metempsicosi: l'anima che attraversa le vite",
                category="Astrologia evolutiva", reading_min=6, published_at=date(2026, 10, 1),
                excerpt=("Da Pitagora ai Veda, l'idea che l'anima ritorni è una delle intuizioni più antiche "
                         "dell'umanità. Che cosa significa davvero «metempsicosi» e che cosa può dirci oggi, "
                         "senza bisogno di crederci per forza."),
                lead=("Da Pitagora ai Veda, l'idea che l'anima ritorni è una delle intuizioni più antiche "
                      "dell'umanità. Proviamo a capire che cosa dice davvero, e che cosa può dirci oggi."),
                body_html=_read("metempsicosi.html"),
                cover="img/metempsicosi.svg",
                cover_alt=("Illustrazione: una spirale dorata con una farfalla al centro e cinque luci lungo il "
                           "percorso, simbolo dell'anima che attraversa le vite"),
                cover_caption=("In greco antico <em>psyché</em> significa sia «anima» sia «farfalla»: per questo la "
                               "farfalla è da sempre il simbolo dell'anima che si trasforma."),
                meta_title="Metempsicosi: cos'è e cosa dice l'astrologia evolutiva – Daliamae",
                meta_description=("Cos'è la metempsicosi, la differenza con la reincarnazione e il legame con i Nodi "
                                  "Lunari dell'astrologia evolutiva. Tre domande per riflettere."),
                keywords="metempsicosi, reincarnazione, nodi lunari, astrologia evolutiva, oroscopo evolutivo",
                published=True, is_sample=True))
        if Video.query.count() == 0:
            db.session.add(Video(
                title="Come nasce Daliamae", sort=1, upload_date=date(2026, 10, 1),
                description="Da dove viene il nome e il progetto Daliamae, raccontato da Dalia.",
                file="video/come-nasce-daliamae.mp4", poster="video/come-nasce-daliamae.jpg"))
            db.session.add(Video(
                title="Stai respirando o credi solo di farlo?", sort=2, upload_date=date(2026, 10, 1),
                description="Un breve video sul respiro e sulla presenza.",
                file="video/stai-respirando.mp4", poster="video/stai-respirando.jpg"))
        db.session.commit()
    except Exception:          # più processi che partono insieme: il primo vince
        db.session.rollback()
