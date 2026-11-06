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
    ("♉︎", "Toro", "Terra", "La Custode", "La calma di radicarsi e di coltivare ciò che ha valore."),
    ("♊︎", "Gemelli", "Aria", "Il Messaggero", "La curiosità che collega idee, persone e parole."),
    ("♋︎", "Cancro", "Acqua", "La Madre", "La capacità di accogliere, nutrire e proteggere."),
    ("♌︎", "Leone", "Fuoco", "Il Sovrano", "La luce di chi si esprime dal cuore."),
    ("♍︎", "Vergine", "Terra", "La Guaritrice", "La cura del dettaglio e il servizio attento."),
    ("♎︎", "Bilancia", "Aria", "L'Amante", "La ricerca di armonia, bellezza e relazione."),
    ("♏︎", "Scorpione", "Acqua", "L'Alchimista", "La forza di attraversare l'ombra e rinascere."),
    ("♐︎", "Sagittario", "Fuoco", "Il Cercatore", "Lo slancio verso il senso e l'orizzonte."),
    ("♑︎", "Capricorno", "Terra", "La Saggia", "La pazienza di costruire e la responsabilità."),
    ("♒︎", "Acquario", "Aria", "Il Visionario", "La libertà di pensare oltre le regole."),
    ("♓︎", "Pesci", "Acqua", "La Mistica", "L'empatia che scioglie i confini."),
]

# Quando si apre una carta: periodo, dono (dalla leggenda della creazione riportata da Martin Schulman,
# solo il nome del dono) e una domanda per te. Il racconto completo resta per gli incontri.
SIGN_DEEP = {
    'Ariete': ('21 marzo – 19 aprile', 'la stima di sé',
              'Che cosa nella tua vita aspetta solo il tuo primo passo?'),
    'Toro': ('20 aprile – 20 maggio', 'la forza',
            'Che cosa ti fa sentire davvero al sicuro, senza bisogno di possederlo?'),
    'Gemelli': ('21 maggio – 20 giugno', 'la conoscenza',
               'Quale parola non hai ancora detto, e a chi?'),
    'Cancro': ('21 giugno – 22 luglio', 'la famiglia',
              'Chi si prende cura della bambina che è in te?'),
    'Leone': ('23 luglio – 22 agosto', "l'onore",
             'Come brilleresti se nessuno ti stesse guardando?'),
    'Vergine': ('23 agosto – 22 settembre', 'la purezza di spirito',
               'Che cosa succederebbe se ti concedessi di essere imperfetta?'),
    'Bilancia': ('23 settembre – 22 ottobre', "l'amore",
                'Dove stai cercando fuori un equilibrio che può nascere solo dentro?'),
    'Scorpione': ('23 ottobre – 21 novembre', 'la determinazione',
                 'Che cosa sei pronta a lasciar andare per rinascere?'),
    'Sagittario': ('22 novembre – 21 dicembre', "l'abbondanza",
                  "Qual è l'orizzonte che ti chiama in questo momento?"),
    'Capricorno': ('22 dicembre – 19 gennaio', 'la responsabilità',
                  'Che cosa stai costruendo, e per chi lo stai facendo davvero?'),
    'Acquario': ('20 gennaio – 18 febbraio', 'la libertà',
                'Dove puoi essere libera e, insieme, vicina?'),
    'Pesci': ('19 febbraio – 20 marzo', 'la comprensione',
             'Quale sogno sta chiedendo di toccare terra?'),
}

# Immagini e video degli archetipi (in static/): compaiono in alto nella carta aperta.
# "fig" = personaggio in miniatura a destra sulla carta chiusa; "img" = immagine; "video" = video breve senza audio che parte da solo (con "img" come copertina);
# "audio": True = il video ha il sonoro: parte muto e compare il tasto 🔈 per ascoltarlo.
# "pos" (facoltativo) = quale parte dell'immagine/video mostrare nella carta aperta, es. "50% 70%" = più in basso.
SIGN_MEDIA = {
    "Ariete": {"fig": "img/archetipi/ariete-figura.jpg", "img": "img/archetipi/ariete.jpg", "video": "video/archetipi/ariete.mp4", "audio": True, "alt": "Video: l'Ariete, guerriero selvaggio nella tempesta, viene avvolto da una spirale di luce e diventa un guerriero luminoso in armatura nel deserto, tra gli arieti"},
    "Toro": {"fig": "img/archetipi/toro-figura.jpg", "img": "img/archetipi/toro.jpg", "video": "video/archetipi/toro.mp4", "audio": True, "alt": "Video: il Toro, donna con corona di fiori e cesto di frutta su una panca di pietra, passa dal cielo grigio allo smarrimento alla luce: tocca la pietra, si radica e sorride nel prato fiorito tra le mucche al pascolo"},
    "Gemelli": {"fig": "img/archetipi/gemelli-figura.jpg", "img": "img/archetipi/gemelli.jpg", "alt": "Illustrazione dei Gemelli: un ragazzo curioso in città con macchina fotografica e tablet, tra farfalle e fiori di primavera, accanto a una bicicletta tandem con il secondo sellino vuoto"},
    "Cancro": {"fig": "img/archetipi/cancro-figura.jpg", "img": "img/archetipi/cancro.jpg", "video": "video/archetipi/cancro.mp4", "audio": True, "pos": "50% 30%", "alt": "Video: il Cancro, giovane donna con scialle rosa, siede triste sulla riva di un lago sotto la luna piena con un ricamo in grembo. Mentre ricama, il suo lavoro interiore di radicamento e di custodia dei propri confini si accende di luce e fa brillare i simboli degli altri segni: la sua trasformazione illumina tutto lo zodiaco. Alla fine sorride, con un coniglio in grembo e tanti coniglietti intorno"},
    "Leone": {"fig": "img/archetipi/leone-figura.jpg", "img": "img/archetipi/leone.jpg", "video": "video/archetipi/leone.mp4", "audio": True, "alt": "Video: il Leone si libera dalla catena e diventa luce, seduto in meditazione in un tempio dorato tra due leoni"},
    "Vergine": {"fig": "img/archetipi/vergine-figura.jpg", "img": "img/archetipi/vergine.jpg", "video": "video/archetipi/vergine.mp4", "audio": True, "pos": "50% 70%", "alt": "Video: la Vergine nel suo studio, tra libri e semi sotto la costellazione, passa dall'ansia del controllo alla quiete quando un raggio di luce la raggiunge"},
    "Bilancia": {"fig": "img/archetipi/bilancia-figura.jpg", "img": "img/archetipi/bilancia.jpg", "video": "video/archetipi/bilancia.mp4", "audio": True, "alt": "Video: la Bilancia, giovane uomo con gilet lilla e mantello verde di foglie d'autunno, chiude gli occhi mentre un nastro di luce dorata lo avvolge, e appare nel giardino di rose tra il giorno e la notte, con la bilancia in mano e una colomba sulla fontana"},
    "Scorpione": {"fig": "img/archetipi/scorpione-figura.jpg", "img": "img/archetipi/scorpione.jpg", "pos": "50% 12%", "alt": "Illustrazione dello Scorpione, l'Alchimista: una giovane donna dai lunghi capelli neri in abito bordeaux ricamato d'oro, inginocchiata sulla riva di un lago scuro in una grotta, tiene tra le mani un'ampolla di luce dorata. Sulla roccia accanto a lei uno scorpione, che riflesso nell'acqua diventa una fenice di fuoco. Sullo sfondo un vulcano e il simbolo dello Scorpione disegnato dalle stelle"},
    "Sagittario": {"fig": "img/archetipi/sagittario-figura.jpg", "img": "img/archetipi/sagittario.jpg", "video": "video/archetipi/sagittario.mp4", "audio": True, "alt": "Video: un centauro in un lago di montagna sotto la luna piena, tra cristalli verdi"},
    "Capricorno": {"fig": "img/archetipi/capricorno-figura.jpg", "img": "img/archetipi/capricorno.jpg", "pos": "50% 30%", "alt": "Illustrazione del Capricorno, la Saggia: una donna matura dai capelli d'argento raccolti in una treccia, con mantello verde scuro ricamato e corde annodate sul petto, in piedi sulla vetta innevata di una montagna all'alba d'inverno, tiene in mano un cristallo che si accende di luce dorata. Ai suoi piedi ha posato il sacco di tela portato durante la salita; accanto a lei uno stambecco, in cielo un corvo e il simbolo del Capricorno disegnato dalle stelle, mentre il sole sorge dietro le vette"},
    "Acquario": {"fig": "img/archetipi/acquario-figura.jpg", "img": "img/archetipi/acquario.jpg", "pos": "50% 20%", "alt": "Illustrazione dell'Acquario, il Visionario: un giovane dai capelli chiari mossi dal vento, con un'aureola dorata e una tuta argentata a fulmini colorati, versa acqua luminosa da due anfore su un paesaggio di ghiaccio di notte. Nel cielo l'aurora boreale e la costellazione dell'Acquario, un dirigibile e un deltaplano; una zebra e un orso polare bevono dall'acqua"},
}

# Polarità: Fuoco e Aria maschili, Terra e Acqua femminili (simbolo, nome, frase quando si filtra)
POLARITY = {"Fuoco": "Maschile", "Aria": "Maschile", "Terra": "Femminile", "Acqua": "Femminile"}
POLARITIES = {
    "Maschile": ("♂", "I segni maschili, di Fuoco e d'Aria, vanno verso il mondo: energia che si espande, agisce, si esprime. Non parla di genere: in ognuno di noi vivono entrambe le forze."),
    "Femminile": ("♀", "I segni femminili, di Terra e d'Acqua, accolgono: energia che raccoglie, custodisce, fa maturare. Non parla di genere: in ognuno di noi vivono entrambe le forze."),
}

# Gli elementi: come si presentano quando si filtrano le carte
ELEMENTS = {
    "Fuoco": "Il Fuoco accende: è slancio, entusiasmo, la scintilla che dà inizio alle cose.",
    "Terra": "La Terra radica: è corpo, concretezza, la pazienza di far crescere.",
    "Aria": "L'Aria collega: è pensiero, parola, incontro tra le persone e le idee.",
    "Acqua": "L'Acqua sente: è emozione, intuizione, la memoria profonda dell'anima.",
}
