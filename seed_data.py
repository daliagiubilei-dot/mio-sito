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
    _update_faq_progetto_animico()
    _update_seo_oroscopo()
    _update_massaggio_prossimamente()


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

CUFFIE_GIUDIZIO_BODY = """
<p>"I giovani sono alienati", "Stanno sempre con le cuffie e la testa tra le nuvole", "Non sanno più comunicare". Quante volte lo abbiamo pensato (o detto)?</p>

<p><strong>Continuiamo a criticare invece di comprendere.</strong></p>

<p>Quelle cuffie sembrano un muro, ma forse sono solo un modo per cercare un po' di silenzio dentro un mondo che urla. Uno spazio tutto loro, dove nessuno li giudica.</p>

<p>Poi li vediamo riunirsi in centinaia per una aura battle, e li giudichiamo anche lì. Se si isolano, sbagliano. Se si incontrano, sbagliano.</p>

<p>Allora facciamo un passo indietro e chiediamoci: cosa cercano davvero?</p>

<h2>Che cosa significa "avere aura"</h2>

<p><strong>Aura</strong> significa "soffio". È quell'energia invisibile che ci circonda, quella che gli altri sentono prima ancora che apriamo bocca. Quando un ragazzo cerca di "avere aura", non sta inseguendo una sciocchezza: sta chiedendo di essere visto per ciò che è, non per la performance che offre.</p>

<h2>Il significato simbolico del "six seven"</h2>

<p>E quel famigerato <strong>"six seven"</strong> che ripetono ovunque? Il 6 è il cuore, il legame, l'appartenenza. Il 7 è la ricerca interiore, il mistero. Insieme fanno 13, il numero della trasformazione.</p>

<p>Forse è solo un tormentone passeggero. O forse, senza saperlo, stanno dando voce proprio a questo passaggio: dal bisogno di appartenere a un gruppo al bisogno di scoprire chi sono davvero.</p>

<blockquote>Ogni generazione ha le sue geografie interiori. Il nostro compito non è correggerle, ma decodificarle.</blockquote>

<p>Non serve guardarle con la sufficienza degli adulti. Togliamoci le nostre di cuffie, quelle del giudizio, della fretta, della presunzione di sapere già tutto, e proviamo ad ascoltare cosa ci stanno urlando in silenzio.</p>

<p>E tu, da che parte stai? Ti fermi a giudicare la superficie o provi a guardare cosa c'è dietro?</p>
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
    dict(
        slug="aura-battle-togliamoci-le-cuffie-del-giudizio",
        title="Aura battle: togliamoci le cuffie del giudizio",
        category="Crescita personale",
        excerpt="Centinaia di ragazzi riuniti per una aura battle, e noi a giudicarli. E se provassimo a capire cosa cercano davvero?",
        lead="Centinaia di ragazzi riuniti per una aura battle. E noi, ancora una volta, a giudicarli.",
        body_html=CUFFIE_GIUDIZIO_BODY.strip(),
        cover="img/blog/cuffie-giudizio-cover.jpg",
        cover_alt="Illustrazione: un ragazzo con le cuffie seduto su un muretto, dietro di lui una folla di ragazzi in cerchio durante una aura battle. In alto la scritta Togliamoci le cuffie del giudizio",
        published_at=date(2026, 10, 19),
        reading_min=3,
        meta_title="Aura battle: togliamoci le cuffie del giudizio – Daliamae",
        meta_description="Aura battle e six seven: cosa cercano davvero i ragazzi? Il significato di aura, la simbologia dei numeri 6 e 7 e l'invito a comprendere invece di giudicare.",
        keywords="aura battle, significato aura, six seven significato, adolescenti, generazione Z, giudizio, comprendere i giovani, numerologia, crescita personale",
    ),
]


VIDEOS = [
    dict(
        key="cambio-di-prospettiva",
        title="Il cambio di prospettiva",
        description="Un breve video di Dalia sul cambio di prospettiva: guardare la stessa situazione da un altro punto di vista.",
        file="video/cambio-di-prospettiva.mp4",
        poster="video/cambio-di-prospettiva.jpg",
        upload_date=date(2026, 10, 11),
        sort=0,                      # 0 = primo della pagina Video Social
    ),
]


def _add_videos():
    for data in VIDEOS:
        data = dict(data)
        key = data.pop("key")
        try:
            if not _first_time("video_" + key) or Video.query.filter_by(file=data["file"]).first():
                db.session.commit()
                continue
            db.session.add(Video(published=True, **data))
            db.session.commit()
        except Exception:      # più processi che partono insieme: il primo vince
            db.session.rollback()


def _add_posts():
    _add_videos()
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


# ---------------------------------------------------------------- FAQ: oroscopo evolutivo come progetto animico
# Aggiorna una sola volta le due risposte sull'oroscopo evolutivo, ma solo se nel pannello
# sono ancora identiche al testo originale (le modifiche fatte da Dalia non vengono toccate).
FAQ_PROGETTO_ANIMICO = [
    ("L'oroscopo evolutivo è una lettura del tema natale che lo interpreta come una mappa di potenzialità e schemi interiori, anziché come previsione di eventi. Aiuta a riconoscere le proprie inclinazioni, i blocchi ricorrenti e le direzioni di crescita, per vivere le scelte con più consapevolezza.",
     "L'oroscopo evolutivo legge il cielo di nascita come il progetto che la tua anima ha scelto prima di incarnarsi: non un destino scritto, ma la direzione che sei qui per abitare. Più che prevedere eventi, il tema natale diventa la mappa di questo progetto: aiuta a riconoscere le tue inclinazioni, i blocchi ricorrenti e le direzioni di crescita, per vivere le scelte con più consapevolezza."),
    ("L'oroscopo classico, come quello dei giornali, parla del segno solare e cerca di prevedere cosa accadrà. L'oroscopo evolutivo studia il tuo tema natale completo, calcolato su data, ora e luogo di nascita, e si concentra su chi sei e su come puoi crescere, non su cosa ti succederà.",
     "L'oroscopo classico, come quello dei giornali, parla del segno solare e cerca di prevedere cosa accadrà. L'oroscopo evolutivo studia il tuo tema natale completo, calcolato su data, ora e luogo di nascita, e lo legge come il progetto della tua anima: si concentra su chi sei, sulle tue inclinazioni e su come puoi crescere, non su cosa ti succederà."),
]


def _update_faq_progetto_animico():
    try:
        if not _first_time("faq_progetto_animico"):
            return
        for old, new in FAQ_PROGETTO_ANIMICO:
            for row in AeoPhrase.query.filter_by(answer=old).all():
                row.answer = new
        db.session.commit()
    except Exception:
        db.session.rollback()


# ---------------------------------------------------------------- SEO: descrizione oroscopo evolutivo
# Aggiorna una sola volta la meta description della pagina, solo se nel pannello è ancora quella originale.
SEO_OROSCOPO_OLD = "Oroscopo evolutivo: la lettura del tema natale come mappa di potenzialità e schemi interiori. Servono data, ora e luogo di nascita. Anche online."
SEO_OROSCOPO_NEW = "Oroscopo evolutivo: il tema natale letto come progetto della tua anima, per riconoscere le tue inclinazioni. Servono data, ora e luogo di nascita. Anche online."


def _update_seo_oroscopo():
    try:
        if not _first_time("seo_oroscopo_progetto_animico"):
            return
        row = PageSEO.query.filter_by(slug="percorsi/oroscopo-evolutivo").first()
        if row and row.meta_description in ("", SEO_OROSCOPO_OLD):
            row.meta_description = SEO_OROSCOPO_NEW
        db.session.commit()
    except Exception:
        db.session.rollback()


# ---------------------------------------------------------------- massaggio psicosomatico: "Prossimamente"
# Aggiorna una sola volta FAQ e SEO già salvati nel database, solo se sono ancora i testi originali
# (se Dalia li ha già cambiati dal pannello, restano come li ha scritti lei).
FAQ_MASSAGGIO_PROSSIMAMENTE = [
    [
        "No. Il massaggio psicosomatico è una pratica di benessere che usa un tocco consapevole per aiutarti a percepire e sciogliere le tensioni legate alle emozioni. Non è un trattamento sanitario o fisioterapico: in presenza di dolori, patologie o disturbi è necessario rivolgersi prima al proprio medico.",
        "No. Il massaggio psicosomatico, disponibile prossimamente, è una pratica di benessere che usa un tocco consapevole per aiutarti a percepire e sciogliere le tensioni legate alle emozioni. Non è un trattamento sanitario o fisioterapico: in presenza di dolori, patologie o disturbi è necessario rivolgersi prima al proprio medico."
    ],
    [
        "Non serve saperlo in anticipo. Nel primo contatto Dalia ascolta cosa stai vivendo e cosa cerchi, e insieme individuate la pratica più adatta: la lettura del tema natale per fare chiarezza, la meditazione per ritrovare calma, il percorso individuale per un cambiamento profondo, il massaggio per ripartire dal corpo.",
        "Non serve saperlo in anticipo. Nel primo contatto Dalia ascolta cosa stai vivendo e cosa cerchi, e insieme individuate la pratica più adatta: la lettura del tema natale per fare chiarezza, la meditazione per ritrovare calma, il percorso individuale per un cambiamento profondo, e, prossimamente, il massaggio per ripartire dal corpo."
    ],
    [
        "La lettura dell'oroscopo evolutivo e i percorsi individuali di consapevolezza si prestano anche all'incontro online, in videochiamata, ovunque tu sia in Italia. Il massaggio psicosomatico si svolge invece solo in presenza. Le modalità disponibili si concordano al momento della prenotazione.",
        "La lettura dell'oroscopo evolutivo e i percorsi individuali di consapevolezza si prestano anche all'incontro online, in videochiamata, ovunque tu sia in Italia. Il massaggio psicosomatico, disponibile prossimamente, si svolgerà invece solo in presenza. Le modalità disponibili si concordano al momento della prenotazione."
    ]
]

SEO_MASSAGGIO_PROSSIMAMENTE = [
    [
        "home",
        "Dalia Giubilei – Operatrice Olistica | Oroscopo Evolutivo",
        "Dalia Giubilei – Operatrice Olistica | Oroscopo Evolutivo",
        "Operatrice olistica: oroscopo evolutivo, meditazioni guidate, percorsi di crescita personale e massaggio psicosomatico per il tuo benessere olistico.",
        "Operatrice olistica: oroscopo evolutivo, meditazioni guidate, percorsi di crescita personale e, prossimamente, massaggio psicosomatico per il tuo benessere olistico."
    ],
    [
        "percorsi",
        "Pratiche e Percorsi | Oroscopo evolutivo e meditazione – Daliamae",
        "Pratiche e Percorsi | Oroscopo evolutivo e meditazione – Daliamae",
        "Oroscopo evolutivo, meditazioni guidate, percorsi individuali di crescita personale e massaggio psicosomatico: quattro strade per tornare al tuo centro.",
        "Oroscopo evolutivo, meditazioni guidate, percorsi individuali di crescita personale e, prossimamente, massaggio psicosomatico: quattro strade per tornare al tuo centro."
    ],
    [
        "percorsi/massaggio-psicosomatico",
        "Massaggio psicosomatico | Tocco consapevole – Daliamae",
        "Massaggio psicosomatico (prossimamente) – Daliamae",
        "Massaggio psicosomatico: un tocco consapevole per percepire e sciogliere le tensioni legate alle emozioni. Pratica di benessere, non sanitaria.",
        "Prossimamente: massaggio psicosomatico, un tocco consapevole per percepire e sciogliere le tensioni legate alle emozioni. Pratica di benessere, non sanitaria."
    ]
]


def _update_massaggio_prossimamente():
    try:
        if not _first_time("massaggio_prossimamente"):
            return
        for old, new in FAQ_MASSAGGIO_PROSSIMAMENTE:
            for row in AeoPhrase.query.filter_by(answer=old).all():
                row.answer = new
        for slug, old_t, new_t, old_d, new_d in SEO_MASSAGGIO_PROSSIMAMENTE:
            row = PageSEO.query.filter_by(slug=slug).first()
            if not row:
                continue
            if row.title in ("", old_t):
                row.title = new_t
            if row.meta_description in ("", old_d):
                row.meta_description = new_d
        db.session.commit()
    except Exception:
        db.session.rollback()
