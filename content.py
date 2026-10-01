"""Contenuti fissi del sito: pratiche, segni zodiacali, argomenti delle FAQ."""

INTERESTS = ["Oroscopo evolutivo", "Meditazioni guidate", "Percorso 1:1",
             "Massaggio psicosomatico", "Non lo so ancora"]

# Argomenti con cui si dividono le domande nella pagina "Domande frequenti"
FAQ_GROUPS = [("op", "L'operatrice"), ("pr", "Le pratiche"), ("cf", "Come funziona")]

SERVICES = {
    "oroscopo-evolutivo": {
        "name": "Oroscopo evolutivo",
        "h1": "Oroscopo evolutivo & Messaggi dell'Anima",
        "intro": "La mappa del cielo come specchio del tuo cammino, dell'inconscio e delle vocazioni interiori.",
        "detail": "Una lettura del tema natale che lo interpreta come mappa di potenzialità e schemi interiori, non come previsione di eventi.",
        "meta": "Serve: data, ora e luogo di nascita.",
        "cta": "Richiedi la lettura",
        "interest": "Oroscopo evolutivo",
    },
    "meditazioni-guidate": {
        "name": "Meditazione guidata",
        "h1": "Meditazioni guidate",
        "intro": "Silenzio, respiro, grounding e visualizzazione per connetterti con la tua parte più profonda, su temi specifici e generali.",
        "detail": "Nella meditazione guidata la voce ti accompagna passo dopo passo attraverso il respiro, il radicamento e la visualizzazione.",
        "meta": "Individuali o di gruppo.",
        "cta": "Chiedi informazioni",
        "interest": "Meditazioni guidate",
    },
    "percorso-individuale": {
        "name": "Percorsi di crescita personale",
        "h1": "Percorsi 1:1 di consapevolezza e crescita",
        "intro": "Incontri individuali di riallineamento, comprensione degli schemi personali e riscoperta del proprio centro.",
        "detail": "Un accompagnamento individuale per riconoscere gli schemi che si ripetono e tornare al proprio centro, con pratiche semplici da portare nella vita di ogni giorno.",
        "meta": "",
        "cta": "Parliamone",
        "interest": "Percorso 1:1",
    },
    "massaggio-psicosomatico": {
        "name": "Massaggio psicosomatico",
        "h1": "Massaggio psicosomatico",
        "intro": "Il corpo come linguaggio: un tocco consapevole per sciogliere tensioni emotive e ritrovare armonia tra corpo e mente.",
        "detail": "Una pratica di benessere che usa un tocco consapevole per aiutarti a percepire e sciogliere le tensioni legate alle emozioni. Non è un trattamento sanitario.",
        "meta": "In presenza.",
        "cta": "Prenota",
        "interest": "Massaggio psicosomatico",
    },
}

# (simbolo, segno, elemento, archetipo, frase)
SIGNS = [
    ("♈︎", "Ariete", "Fuoco", "Il Guerriero", "Il coraggio di iniziare e di affermare chi sei."),
    ("♉︎", "Toro", "Terra", "Il Custode", "La calma di radicarsi e di coltivare ciò che ha valore."),
    ("♊︎", "Gemelli", "Aria", "Il Messaggero", "La curiosità che collega idee, persone e parole."),
    ("♋︎", "Cancro", "Acqua", "La Madre", "La capacità di accogliere, nutrire e proteggere."),
    ("♌︎", "Leone", "Fuoco", "Il Sovrano", "La luce di chi si esprime dal cuore."),
    ("♍︎", "Vergine", "Terra", "La Guaritrice", "La cura del dettaglio e il servizio attento."),
    ("♎︎", "Bilancia", "Aria", "L'Amante", "La ricerca di armonia, bellezza e relazione."),
    ("♏︎", "Scorpione", "Acqua", "L'Alchimista", "La forza di attraversare l'ombra e rinascere."),
    ("♐︎", "Sagittario", "Fuoco", "Il Cercatore", "Lo slancio verso il senso e l'orizzonte."),
    ("♑︎", "Capricorno", "Terra", "Il Saggio", "La pazienza di costruire e la responsabilità."),
    ("♒︎", "Acquario", "Aria", "Il Visionario", "La libertà di pensare oltre le regole."),
    ("♓︎", "Pesci", "Acqua", "Il Mistico", "L'empatia che scioglie i confini."),
]
