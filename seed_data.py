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
    _add_posts()


# ---------------------------------------------------------------- articoli aggiunti dal codice
# Ogni articolo viene inserito una sola volta (se non esiste già con lo stesso slug).
# Dopo, si modifica o si elimina dal pannello /admin/blog e non viene più ricreato.

CRISI_BUSSOLA_BODY = """
<p>Spesso guardiamo al blocco, al momento di transizione o al caos improvviso come a un errore da correggere, a un ingranaggio spezzato nella nostra vita. Ci sentiamo fuori asse, persi in un labirinto di aspettative — sul lavoro, nelle relazioni, nei traguardi da rispettare a tutti i costi. Cerchiamo risposte lampo, scorciatoie per spegnere il disagio, dimenticando che ciò che si affretta rischia di non radicarsi mai davvero.</p>

<figure class="post-pair">
  <img src="/static/img/blog/crisi-bussola-corsa.jpg" alt="Un coniglio bianco corre nel bosco guardando preoccupato il suo orologio da taschino" loading="lazy" width="720" height="1263">
  <img src="/static/img/blog/crisi-bussola-scoperta.jpg" alt="Il coniglio bianco si ferma e scopre che l'orologio è una bussola dorata con la scritta Crisi" loading="lazy" width="720" height="1253">
  <figcaption>Prima la corsa contro il tempo, poi la scoperta: l'orologio era una bussola.</figcaption>
</figure>

<p>Eppure, ogni cambiamento esteriore ha una radice profonda che risuona nel nostro spazio interiore. La crisi non è un ritardo sulla tabella di marcia, né una condanna da subire. È il momento esatto in cui il caos esteriore si placa quel tanto che basta per mostrarti uno specchio: la tua vera rotta.</p>

<blockquote>La crisi non è un ritardo sulla tabella di marcia: è lo specchio che ti mostra la tua vera rotta.</blockquote>

<p>Quando smetti di lottare contro la corrente e inizi a decifrare i simboli che il tuo stesso vissuto ti sta ponendo davanti, tutto si riconfigura. Ciò che prima ti spaventava — il vuoto, la fine di un ciclo, l'incertezza — si trasforma in materia viva, pronta a rigenerarsi.</p>

<p>Il microcosmo della tua esperienza quotidiana e il macrocosmo delle tue aspirazioni profonde tornano finalmente a parlarsi. Non devi decifrare questo linguaggio da solo o da sola.</p>

<p>✨ <strong>Vuoi fare chiarezza e ritrovare il tuo centro?</strong> <a href="/contatti?pratica=Percorso+1%3A1">Scrivimi</a>: il primo incontro orientativo è completamente gratuito.</p>
"""

POSTS = [
    dict(
        slug="crisi-vera-bussola",
        title="E se la crisi fosse la tua vera bussola?",
        category="Crescita personale",
        excerpt="Il blocco, la transizione, il caos improvviso non sono errori da correggere: possono essere lo specchio che ti mostra la tua vera rotta.",
        lead="Come in alto, così dentro. Quante volte ti ritrovi a correre, inseguendo il ticchettio di un tempo che sembra non bastare mai, con il fiatone di chi sta cercando di incastrare la propria essenza in forme e standard che non ha scelto?",
        body_html=CRISI_BUSSOLA_BODY.strip(),
        cover="img/blog/crisi-bussola-cover.jpg",
        cover_alt="Coniglio bianco nel bosco che tiene tra le mani una bussola dorata con la scritta Crisi",
        published_at=date(2026, 10, 11),
        reading_min=3,
        meta_title="E se la crisi fosse la tua vera bussola? – Daliamae",
        meta_description="La crisi non è un errore da correggere: è lo specchio che mostra la tua vera rotta. Una riflessione di crescita personale e trasformazione interiore.",
        keywords="crescita personale, crescita interiore, trasformazione interiore, simbolismo, consapevolezza, crisi come opportunità, ascolto autentico",
    ),
]


def _add_posts():
    from models import Post
    for data in POSTS:
        try:
            if not _first_time("post_" + data["slug"]) or Post.query.filter_by(slug=data["slug"]).first():
                db.session.commit()
                continue
            db.session.add(Post(published=True, is_sample=False, **data))
            db.session.commit()
        except Exception:      # più processi che partono insieme: il primo vince
            db.session.rollback()
