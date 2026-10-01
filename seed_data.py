"""Riempie il database al primo avvio con i contenuti del prototipo."""
import json
import os
from datetime import date

from models import db, PageSEO, AeoPhrase, Video, Setting
from seo import PAGE_DEFAULTS, CORE_KEYWORDS

SEED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed")


def _read(name):
    with open(os.path.join(SEED_DIR, name), encoding="utf-8") as f:
        return f.read()


def _first_time(key):
    """True solo la prima volta per ogni gruppo di contenuti. Poi il gruppo non viene più ricreato,
    nemmeno se Dalia elimina tutto dal pannello (altrimenti i contenuti eliminati tornerebbero a ogni riavvio)."""
    flag = "seeded_" + key
    if Setting.query.filter_by(key=flag).first():
        return False
    db.session.add(Setting(key=flag, value="1"))
    return True


def seed_if_empty():
    try:
        if _first_time("pages") and PageSEO.query.count() == 0:
            for slug, (label, title, desc, kw) in PAGE_DEFAULTS.items():
                db.session.add(PageSEO(slug=slug, label=label, title=title, meta_description=desc, keywords=kw))
        if _first_time("keywords") and Setting.query.filter_by(key="keywords").first() is None:
            db.session.add(Setting(key="keywords", value="\n".join(CORE_KEYWORDS)))
        if _first_time("aeo") and AeoPhrase.query.count() == 0:
            for item in json.loads(_read("aeo.json")):
                db.session.add(AeoPhrase(question=item["question"], answer=item["answer"], group=item["group"],
                                         page_slugs=",".join(item["pages"]), sort=item["sort"], published=True))
        if _first_time("videos") and Video.query.count() == 0:
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
