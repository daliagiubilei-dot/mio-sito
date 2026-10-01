"""SEO: parole chiave del settore olistico, testi di default per ogni pagina e dati strutturati (JSON-LD).

Le parole chiave e i testi qui sotto sono solo il PUNTO DI PARTENZA: al primo avvio vengono copiati nel
database e da lì si modificano dal pannello di controllo (/admin), senza toccare il codice.
"""

# Parole chiave principali del settore (modificabili dal pannello: sezione "Parole chiave")
CORE_KEYWORDS = [
    "operatrice olistica",
    "oroscopo evolutivo",
    "astrologia evolutiva",
    "lettura del tema natale",
    "tema natale online",
    "nodi lunari",
    "archetipi astrologici",
    "meditazione guidata",
    "meditazione di gruppo",
    "percorso di crescita personale",
    "crescita personale online",
    "percorso olistico di consapevolezza",
    "massaggio psicosomatico",
    "tocco consapevole",
    "benessere olistico",
    "eventi olistici",
]

# slug della pagina -> (etichetta, title ≤ 60 caratteri circa, description ≤ 155, parole chiave)
PAGE_DEFAULTS = {
    "home": ("Home",
        "Dalia Giubilei – Operatrice Olistica | Oroscopo Evolutivo",
        "Operatrice olistica: oroscopo evolutivo, meditazioni guidate, percorsi di crescita personale e massaggio psicosomatico per il tuo benessere olistico.",
        "operatrice olistica, oroscopo evolutivo, meditazione guidata, crescita personale, massaggio psicosomatico, benessere olistico"),
    "la-visione": ("La Visione",
        "La Visione | Percorsi olistici di consapevolezza – Daliamae",
        "Un percorso olistico di consapevolezza unisce corpo, emozioni e dimensione interiore per ritrovare il proprio centro. Scopri la visione di Daliamae.",
        "percorso olistico, percorso di consapevolezza, crescita personale, benessere olistico, cammino interiore"),
    "chi-sono": ("Chi sono",
        "Chi sono | Dalia Giubilei, Operatrice Olistica – Daliamae",
        "Dalia Giubilei, operatrice olistica ai sensi della L. 4/2013. In formazione olistica dal 2019, con oltre 25 anni di esperienza professionale.",
        "operatrice olistica, Dalia Giubilei, formazione olistica, crescita personale"),
    "percorsi": ("Pratiche & Percorsi",
        "Pratiche e Percorsi | Oroscopo evolutivo e meditazione – Daliamae",
        "Oroscopo evolutivo, meditazioni guidate, percorsi individuali di crescita personale e massaggio psicosomatico: quattro strade per tornare al tuo centro.",
        "oroscopo evolutivo, meditazione guidata, percorso di crescita personale, massaggio psicosomatico"),
    "percorsi/oroscopo-evolutivo": ("Pratica: Oroscopo evolutivo",
        "Oroscopo evolutivo | Lettura del tema natale online – Daliamae",
        "Oroscopo evolutivo: la lettura del tema natale come mappa di potenzialità e schemi interiori. Servono data, ora e luogo di nascita. Anche online.",
        "oroscopo evolutivo, lettura del tema natale, tema natale online, astrologia evolutiva, nodi lunari"),
    "percorsi/meditazioni-guidate": ("Pratica: Meditazioni guidate",
        "Meditazione guidata | Individuale e di gruppo – Daliamae",
        "Meditazione guidata individuale e di gruppo: respiro, radicamento e visualizzazione per ritrovare calma e presenza. Nessuna esperienza richiesta.",
        "meditazione guidata, meditazione di gruppo, respiro, grounding, visualizzazione"),
    "percorsi/percorso-individuale": ("Pratica: Percorso 1:1",
        "Percorso di crescita personale 1:1 online – Daliamae",
        "Percorso individuale di consapevolezza e crescita personale online: incontri 1:1 per riconoscere gli schemi che si ripetono e tornare al tuo centro.",
        "percorso di crescita personale, percorso di consapevolezza, crescita personale online, incontri individuali"),
    "percorsi/massaggio-psicosomatico": ("Pratica: Massaggio psicosomatico",
        "Massaggio psicosomatico | Tocco consapevole – Daliamae",
        "Massaggio psicosomatico: un tocco consapevole per percepire e sciogliere le tensioni legate alle emozioni. Pratica di benessere, non sanitaria.",
        "massaggio psicosomatico, tocco consapevole, benessere corpo mente, benessere olistico"),
    "archetipi-astrologici": ("Archetipi astrologici",
        "Archetipi astrologici | I 12 segni zodiacali – Daliamae",
        "Dodici archetipi astrologici, dal Guerriero al Mistico: i segni zodiacali letti con l'astrologia evolutiva come modi di stare al mondo e di crescere.",
        "archetipi astrologici, segni zodiacali, astrologia evolutiva, elementi fuoco terra aria acqua"),
    "eventi": ("Eventi",
        "Eventi olistici | Meditazioni di gruppo e incontri – Daliamae",
        "Meditazioni di gruppo ed eventi olistici con Dalia Giubilei: date, luoghi e posti disponibili. Nessuna esperienza richiesta.",
        "eventi olistici, meditazione di gruppo, meditazione guidata, incontri di consapevolezza"),
    "blog": ("Blog",
        "Blog | Astrologia evolutiva e crescita personale – Daliamae",
        "Un articolo al mese su astrologia evolutiva, meditazione guidata e crescita personale, per prendersi il tempo di leggere.",
        "astrologia evolutiva, meditazione guidata, crescita personale, blog olistico"),
    "video-social": ("Video Social",
        "Video Social | Meditazione e astrologia evolutiva – Daliamae",
        "Brevi video di meditazione, astrologia evolutiva e consapevolezza: una selezione dai canali TikTok e Instagram di Daliamae.",
        "video meditazione, astrologia evolutiva, consapevolezza, crescita personale"),
    "domande-frequenti": ("Domande frequenti",
        "Domande frequenti | Oroscopo evolutivo e meditazione – Daliamae",
        "Cosa fa un'operatrice olistica, cos'è l'oroscopo evolutivo, come funziona la meditazione guidata: le risposte alle domande più frequenti.",
        "operatrice olistica, oroscopo evolutivo, meditazione guidata, domande frequenti"),
    "contatti": ("Contatti",
        "Contatti | Primo colloquio con Dalia Giubilei – Daliamae",
        "Prenota un primo colloquio con Dalia Giubilei, operatrice olistica: scrivi su WhatsApp o compila il modulo e scegli insieme la pratica più adatta a te.",
        "operatrice olistica, primo colloquio, prenota, contatti"),
}

# Pagine da NON mostrare nella mappa del sito
NOINDEX = set()


# ---------------------------------------------------------------- dati strutturati (JSON-LD)
def ld_organization(site, base_url, keywords):
    same_as = [u for u in (site["instagram"], site["tiktok"], site["facebook"]) if u]
    person = {
        "@type": "Person", "@id": base_url + "/#dalia", "name": site["owner"], "jobTitle": site["role"],
        "description": "Operatrice olistica ai sensi della Legge 4/2013: oroscopo evolutivo, meditazioni guidate, "
                       "percorsi di crescita personale, massaggio psicosomatico.",
        "url": base_url + "/", "sameAs": same_as, "worksFor": {"@id": base_url + "/#daliamae"},
    }
    business = {
        "@type": "ProfessionalService", "@id": base_url + "/#daliamae", "name": site["name"], "url": base_url + "/",
        "description": "Percorsi olistici di consapevolezza: oroscopo evolutivo, meditazioni guidate, "
                       "percorsi individuali di crescita personale e massaggio psicosomatico.",
        "founder": {"@id": base_url + "/#dalia"}, "telephone": site["phone_intl"], "vatID": "IT" + site["vat"],
        "areaServed": "IT", "inLanguage": "it", "sameAs": same_as,
        "knowsAbout": list(keywords)[:14],
        "contactPoint": {"@type": "ContactPoint", "telephone": site["phone_intl"],
                         "contactType": "customer service", "availableLanguage": "it"},
    }
    return {"@context": "https://schema.org", "@graph": [person, business]}


def ld_website(site, base_url):
    return {"@context": "https://schema.org", "@type": "WebSite", "name": site["name"], "url": base_url + "/",
            "inLanguage": "it", "publisher": {"@id": base_url + "/#daliamae"}}


def ld_breadcrumb(base_url, trail):
    """trail = [(nome, url_assoluto), ...] dal primo livello all'ultimo."""
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": base_url + "/"}]
    for i, (name, url) in enumerate(trail, start=2):
        items.append({"@type": "ListItem", "position": i, "name": name, "item": url})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def ld_faq(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f.question,
         "acceptedAnswer": {"@type": "Answer", "text": f.answer}} for f in faqs]}


def ld_article(post, url, image, base_url):
    d = {"@context": "https://schema.org", "@type": "Article", "headline": post.title,
         "description": post.meta_description or post.excerpt, "inLanguage": "it",
         "author": {"@id": base_url + "/#dalia"}, "publisher": {"@id": base_url + "/#daliamae"},
         "mainEntityOfPage": url}
    if post.published_at:
        d["datePublished"] = post.published_at.isoformat()
    if post.updated_at:
        d["dateModified"] = post.updated_at.date().isoformat()
    if image:
        d["image"] = image
    if post.keywords:
        d["keywords"] = post.keywords
    return d


def ld_event(ev, url, base_url):
    d = {"@context": "https://schema.org", "@type": "Event", "name": ev.title, "inLanguage": "it",
         "startDate": ev.starts_at.isoformat(timespec="minutes"),
         "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode" if ev.online
         else "https://schema.org/OfflineEventAttendanceMode",
         "eventStatus": "https://schema.org/EventScheduled",
         "organizer": {"@id": base_url + "/#dalia"}, "url": url}
    if ev.description:
        d["description"] = ev.description
    if ev.place:
        d["location"] = {"@type": "Place", "name": ev.place}
    elif ev.online:
        d["location"] = {"@type": "VirtualLocation", "url": url}
    return d


def ld_video(v, file_url, poster_url, page_url):
    d = {"@context": "https://schema.org", "@type": "VideoObject", "name": v.title,
         "description": v.description or v.title, "contentUrl": file_url, "inLanguage": "it"}
    if poster_url:
        d["thumbnailUrl"] = poster_url
    if v.upload_date:
        d["uploadDate"] = v.upload_date.isoformat()
    return d


def ld_service(svc, url, base_url):
    return {"@context": "https://schema.org", "@type": "Service", "name": svc["h1"],
            "description": svc["intro"], "url": url, "inLanguage": "it", "areaServed": "IT",
            "provider": {"@id": base_url + "/#daliamae"}}
