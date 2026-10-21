"""Contenuti fissi del sito: pratiche, segni zodiacali, argomenti delle FAQ."""

INTERESTS = ["Oroscopo evolutivo", "Meditazioni guidate", "Percorso 1:1",
             "Massaggio psicosomatico (prossimamente)", "Non lo so ancora"]

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
        "name": "Massaggio psicosomatico (prossimamente)",
        "h1": "Massaggio psicosomatico",
        "soon": True,
        "intro": "Il corpo come linguaggio: un tocco consapevole per sciogliere tensioni emotive e ritrovare armonia tra corpo e mente.",
        "detail": "Una pratica di benessere che usa un tocco consapevole per aiutarti a percepire e sciogliere le tensioni legate alle emozioni. Non è un trattamento sanitario.",
        "meta": "Prossimamente · In presenza.",
        "cta": "Prossimamente",
        "interest": "Massaggio psicosomatico (prossimamente)",
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

# Immagini e video dei personaggi-archetipo, per segno (percorsi relativi a /static).
# Per aggiungere un nuovo segno basta una voce con la stessa forma.
SIGN_MEDIA = {
    "Leone": {
        "cover": "img/archetipi/leone/copertina.jpg",
        "teaser": "Dall'ombra alla luce: quando il sole smette di essere una catena.",
        "videos": [
            {"src": "video/archetipi/leone-dall-ombra-alla-luce.mp4",
             "poster": "video/archetipi/leone-dall-ombra-alla-luce.jpg",
             "title": "Dall'ombra alla luce", "vertical": False},
            {"src": "video/archetipi/leone-il-sole-si-libera.mp4",
             "poster": "video/archetipi/leone-il-sole-si-libera.jpg",
             "title": "Il sole si libera", "vertical": True},
        ],
        "images": [
            {"src": "img/archetipi/leone/ombra-e-luce.jpg", "alt": "Il Leone diviso tra ufficio in tempesta e tempio dorato"},
            {"src": "img/archetipi/leone/il-sovrano.jpg", "alt": "Il Leone sorridente nel suo ufficio, in abito blu e cravatta d'oro"},
            {"src": "img/archetipi/leone/il-cuore-solare.jpg", "alt": "Il Leone in meditazione in un tempio di luce, con un sole alle spalle"},
            {"src": "img/archetipi/leone/la-luce-che-insegna.jpg", "alt": "Il Leone che racconta ai bambini, con un libro e un sole sulla copertina"},
        ],
    },
}
