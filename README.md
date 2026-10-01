# Daliamae – sito web (Flask + PostgreSQL)

Sito di Dalia Giubilei, operatrice olistica. Python/Flask, database PostgreSQL su Railway,
pannello di controllo per SEO, frasi chiave AEO, blog, video ed eventi.

## Cosa contiene

| Cosa | Dove |
|---|---|
| Pagine pubbliche | `/`, `/la-visione`, `/chi-sono`, `/percorsi` (+ 4 pagine pratica), `/archetipi-astrologici`, `/eventi`, `/blog`, `/video-social`, `/domande-frequenti`, `/contatti` |
| Pannello di controllo | `/admin` (accesso con `ADMIN_USERNAME` e `ADMIN_PASSWORD`) |
| SEO delle pagine | `/admin/pagine`: title, meta description e parole chiave di ogni pagina |
| Frasi chiave AEO | `/admin/aeo`: domande e risposte dirette, con contatore parole (ideale 40–60), scelta delle pagine in cui compaiono e idee di domande da coprire |
| Parole chiave del settore | `/admin/parole-chiave`; il cruscotto mostra quante volte compaiono nei testi |
| Blog, Video, Eventi | `/admin/blog`, `/admin/video`, `/admin/eventi` |
| Richieste del modulo contatti | `/admin/richieste` (salvate nel database, email di avviso facoltativa) |
| File per Google e AI | `/sitemap.xml`, `/robots.txt`, `/llms.txt` (costruito dalle frasi AEO) |

Per Google e per gli assistenti AI ogni pagina ha: title e meta description propri, canonical, Open Graph e dati
strutturati (`ProfessionalService`/`Person`, `BreadcrumbList`, `FAQPage`, `Article`, `Event`, `VideoObject`, `Service`).
Il markup FAQ viene scritto solo nelle pagine in cui le domande sono davvero visibili.

## Pubblicare su Railway

1. **GitHub**: carica questa cartella nel repository (vedi sotto).
2. **Railway** → *New Project* → *Deploy from GitHub repo* → scegli il repository.
3. Nello stesso progetto: *+ New* → *Database* → *Add PostgreSQL*.
4. Apri il servizio del sito → scheda **Variables** e aggiungi:
   - `DATABASE_URL` = `${{Postgres.DATABASE_URL}}` (riferimento al database; "Postgres" è il nome del servizio database)
   - `SECRET_KEY` = una stringa lunga e casuale
   - `ADMIN_PASSWORD` = la password per entrare in `/admin` (lunga!)
   - (facoltative) `ADMIN_USERNAME` (default `dalia`), `SITE_URL` (es. `https://www.tuodominio.it`), `FACEBOOK_URL`,
     e per le email di avviso `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `MAIL_TO`
5. *Settings → Networking → Generate Domain* (poi, se vuoi, *Custom Domain*).
6. Al primo avvio le tabelle vengono create e riempite con i contenuti del prototipo. Controlla `/healthz`.

Dopo aver collegato il dominio vero, imposta `SITE_URL`: serve a canonical, sitemap e dati strutturati.

## Mettere il codice su GitHub

Dal computer, dentro la cartella del progetto:

```bash
git init
git add .
git commit -m "Primo sito Daliamae"
git branch -M main
git remote add origin https://github.com/daliagiubilei-dot/mio-sito.git
git push -u origin main
```
(oppure con GitHub Desktop: *Add local repository* → *Publish*). Dal browser, "Upload files" ha un limite di 25 MB per file.

## Provarlo sul computer

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
ADMIN_PASSWORD=prova python app.py                     # http://127.0.0.1:5000
```
In locale, senza `DATABASE_URL`, usa un file SQLite (`local.db`), ignorato da Git.

## Video e immagini

- I file stanno in `static/video` e `static/img`. In `static/video` ci sono gli originali.
- Per aggiungere un video: metti il file (e una copertina `.jpg`) in `static/video`, fai commit su GitHub, poi in
  `/admin/video` crea la scheda indicando `video/nome-file.mp4`.
- **Non caricare file dal pannello**: il disco di Railway si azzera a ogni nuova pubblicazione. Per molti video
  conviene un servizio dedicato (es. Cloudflare R2/Stream) e il link diretto nel campo "File video".
- GitHub accetta file fino a 100 MB.

## Da completare prima di andare online

- Pagine **Privacy policy** e **Cookie policy** (ora nel piede di pagina sono solo testo) e informativa del modulo contatti.
- Il sito carica i font da Google Fonts: per il GDPR meglio ospitarli sul sito.
- Testi con "da completare": formazione di Dalia (scuole, corsi, anni), durate e costi, quali pratiche si fanno online,
  riservatezza e privacy. Si trovano nelle frasi AEO (`/admin/aeo`) e nelle pagine pratica.
- **Indirizzo o città**: serve per SEO locale e Google Business Profile.
- Foto originali ad alta risoluzione; testi dei 12 archetipi da riscrivere con la voce di Dalia.
- Articolo di esempio sulla metempsicosi: modificalo, mettilo in bozza o eliminalo da `/admin/blog`.
- Link Facebook: imposta `FACEBOOK_URL` e l'icona compare.

## Sicurezza

- Pannello con password da variabile d'ambiente, protezione CSRF, limite ai tentativi di accesso, cookie `Secure/HttpOnly`.
- Il modulo contatti ha un campo trappola anti-bot e un limite di richieste per indirizzo.
- Non caricare mai `.env` né password o token su GitHub.
