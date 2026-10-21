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

# Approfondimento di ogni archetipo (si apre toccando la carta): periodo, luce, ombra, domanda per te
SIGN_DEEP = {
    "Ariete": ("21 marzo – 19 aprile",
               "L'inclinazione a cominciare: accendere ciò che ancora non c'è, esporsi per primo, dire «io ci sono».",
               "L'impazienza e la fretta che brucia le tappe; la rabbia che arriva prima dell'ascolto.",
               "Che cosa nella tua vita aspetta solo il tuo primo passo?"),
    "Toro": ("20 aprile – 20 maggio",
             "L'inclinazione a radicarsi: dare valore al corpo, ai sensi, a ciò che cresce con il tempo.",
             "L'attaccamento e la paura del cambiamento; trattenere per sentirsi al sicuro.",
             "Che cosa ti fa sentire davvero al sicuro, senza bisogno di possederlo?"),
    "Gemelli": ("21 maggio – 20 giugno",
                "L'inclinazione a mettere in relazione: tradurre, raccontare, far circolare idee e incontri.",
                "La dispersione e la superficialità; parlare per non sentire.",
                "Quale parola non hai ancora detto, e a chi?"),
    "Cancro": ("21 giugno – 22 luglio",
               "L'inclinazione a prendersi cura: creare un nido, nutrire, custodire la memoria delle radici.",
               "Il guscio che si chiude, la nostalgia che trattiene; accudire gli altri per non guardare sé.",
               "Chi si prende cura della bambina che è in te?"),
    "Leone": ("23 luglio – 22 agosto",
              "L'inclinazione a risplendere: esprimere la propria creatività e scaldare chi ci sta accanto.",
              "Il bisogno di approvazione e di applauso; confondere il cuore con l'immagine.",
              "Come brilleresti se nessuno ti stesse guardando?"),
    "Vergine": ("23 agosto – 22 settembre",
                "L'inclinazione a guarire attraverso la cura: ordinare, discernere, mettersi al servizio.",
                "Il perfezionismo e la critica, soprattutto verso se stessi; non sentirsi mai abbastanza.",
                "Che cosa succederebbe se ti concedessi di essere imperfetta?"),
    "Bilancia": ("23 settembre – 22 ottobre",
                 "L'inclinazione all'incontro: cercare armonia, bellezza, giustizia nelle relazioni.",
                 "L'indecisione e il compiacere; rinunciare a sé per non creare conflitto.",
                 "Dove stai cercando fuori un equilibrio che può nascere solo dentro?"),
    "Scorpione": ("23 ottobre – 21 novembre",
                  "L'inclinazione alla trasformazione: scendere in profondità, lasciar morire ciò che è finito, rinascere.",
                  "Il controllo, la gelosia, il rancore che avvelena; la paura di affidarsi.",
                  "Che cosa sei pronta a lasciar andare per rinascere?"),
    "Sagittario": ("22 novembre – 21 dicembre",
                   "L'inclinazione alla ricerca: viaggiare, dentro e fuori, per trovare un senso più grande.",
                   "La fuga in avanti e l'eccesso; la verità brandita come certezza assoluta.",
                   "Qual è l'orizzonte che ti chiama in questo momento?"),
    "Capricorno": ("22 dicembre – 19 gennaio",
                   "L'inclinazione a costruire: dare forma, struttura e durata ai propri sogni.",
                   "La rigidità e il dovere che soffoca; il cuore messo da parte per arrivare in cima.",
                   "Che cosa stai costruendo, e per chi lo stai facendo davvero?"),
    "Acquario": ("20 gennaio – 18 febbraio",
                 "L'inclinazione a innovare: pensare oltre gli schemi, sentirsi parte di qualcosa di più grande.",
                 "Il distacco emotivo e la ribellione fine a se stessa; sentirsi sempre fuori posto.",
                 "Dove puoi essere libera e, insieme, vicina?"),
    "Pesci": ("19 febbraio – 20 marzo",
              "L'inclinazione all'unione: sentire l'altro, sognare, aprirsi all'invisibile e alla compassione.",
              "La confusione e la fuga dalla realtà; perdersi negli altri fino a dimenticarsi.",
              "Quale sogno sta chiedendo di toccare terra?"),
}

# Gli elementi: come si presentano quando si filtrano le carte
ELEMENTS = {
    "Fuoco": "Il Fuoco accende: è slancio, entusiasmo, la scintilla che dà inizio alle cose.",
    "Terra": "La Terra radica: è corpo, concretezza, la pazienza di far crescere.",
    "Aria": "L'Aria collega: è pensiero, parola, incontro tra le persone e le idee.",
    "Acqua": "L'Acqua sente: è emozione, intuizione, la memoria profonda dell'anima.",
}
