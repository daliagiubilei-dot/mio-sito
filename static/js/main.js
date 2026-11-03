// Daliamae – comportamenti della pagina (nessuna dipendenza esterna)
(function () {
  'use strict';

  // Tema: ricorda la scelta fatta con il pulsante "Tema"
  var themeBtn = document.getElementById('themeBtn');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var r = document.documentElement;
      var cur = r.dataset.theme || (matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
      r.dataset.theme = cur === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('dm-theme', r.dataset.theme); } catch (e) {}
    });
  }

  // Menu su telefono: il pulsante "Menu" apre e chiude il pannello delle voci
  var menuBtn = document.getElementById('menuBtn');
  var header = document.querySelector('header.nav');
  function setMenu(open) {
    if (!header || !menuBtn) return;
    header.classList.toggle('open', open);
    menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    menuBtn.setAttribute('aria-label', open ? 'Chiudi il menu' : 'Apri il menu');
  }
  if (menuBtn && header) {
    menuBtn.addEventListener('click', function (e) { e.stopPropagation(); setMenu(!header.classList.contains('open')); });
    header.querySelectorAll('nav a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    document.addEventListener('click', function (e) { if (!header.contains(e.target)) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  }

  // Altezza del menu (serve alle pagine "a schermo intero")
  function setNavH() {
    var h = document.querySelector('header.nav');
    if (h) document.documentElement.style.setProperty('--navh', h.offsetHeight + 'px');
  }
  setNavH();
  addEventListener('resize', setNavH);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(setNavH);

  // FAQ: schede per argomento e una sola risposta aperta per volta
  var tabs = document.querySelectorAll('.faq-tabs button');
  tabs.forEach(function (b) {
    b.addEventListener('click', function () {
      tabs.forEach(function (x) { x.setAttribute('aria-selected', x === b); });
      document.querySelectorAll('.faq-panel').forEach(function (p) { p.hidden = p.id !== 'fp-' + b.dataset.tab; });
    });
  });
  document.querySelectorAll('.faq-panel details').forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (d.open) d.parentElement.querySelectorAll('details').forEach(function (o) { if (o !== d) o.open = false; });
    });
  });

  // Archetipi: filtro per elemento (con la frase che lo presenta) e carte che si aprono in una scheda
  var z = document.getElementById('zodiac');
  var archEl = document.getElementById('archData');
  var arch = { signs: [], elements: {} };
  try { if (archEl) arch = JSON.parse(archEl.textContent); } catch (e) {}
  var elLine = document.getElementById('elLine');
  var slugOf = function (el) { return (el || '').toLowerCase(); };
  if (z) z.querySelectorAll('.sign').forEach(function (c, i) { c.style.setProperty('--d', i); });
  document.querySelectorAll('.filters button').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.filters button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      var el = b.dataset.el, pol = b.dataset.pol;
      if (z) z.querySelectorAll('.sign').forEach(function (c) {
        c.hidden = pol ? c.dataset.pol !== pol : !(el === 'tutti' || c.dataset.el === el);
      });
      if (elLine) {
        elLine.className = 'el-line' + (el && el !== 'tutti' ? ' el-' + slugOf(el) : '') + (pol ? ' pol-line' : '');
        elLine.textContent = pol ? ((arch.polarities || {})[pol] || '') : (el === 'tutti' ? '' : (arch.elements[el] || ''));
      }
    });
  });

  var dlg = document.getElementById('archDlg');
  if (dlg && z && arch.signs.length && typeof dlg.showModal === 'function') {
    var cur = 0, opener = null;
    var visible = function () {
      return Array.prototype.filter.call(z.querySelectorAll('.sign'), function (c) { return !c.hidden; })
        .map(function (c) { return +c.dataset.i; });
    };
    var $ = function (id) { return document.getElementById(id); };
    var soundOn = false;   // se la persona ha attivato l'audio, resta attivo passando alle altre carte
    var show = function (i) {
      var s = arch.signs[i], list = visible();
      cur = i;
      $('adCard').className = 'ad-card el-' + slugOf(s.element);
      $('adWm').textContent = s.symbol;
      $('adEl').textContent = s.element;
      $('adPol').textContent = s.pol_sym; $('adPol').title = 'Segno ' + s.polarity.toLowerCase();
      $('adPeriod').textContent = s.period;
      $('adName').textContent = s.name;
      $('adArc').textContent = s.archetype;
      $('adTxt').textContent = s.text;
      $('adGift').textContent = s.gift;
      var m = $('adMedia'), md = s.media;
      m.innerHTML = '';
      m.hidden = !md;
      $('adCard').classList.toggle('has-m', !!md);
      dlg.classList.toggle('has-m', !!md);
      if (md) {
        var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
        var el, paintSound = null;
        if (md.video && !still) {
          el = document.createElement('video');
          el.src = md.video; el.poster = md.img;
          el.muted = true; el.loop = true; el.autoplay = true; el.playsInline = true;
          el.setAttribute('playsinline', ''); el.setAttribute('aria-label', md.alt);
        } else {
          el = document.createElement('img');
          el.src = md.img; el.alt = md.alt; el.decoding = 'async';
        }
        if (md.pos) el.style.objectPosition = md.pos;
        m.appendChild(el);
        if (md.audio && el.tagName === 'VIDEO') {
          var snd = document.createElement('button');
          snd.type = 'button'; snd.className = 'ad-sound';
          var paint = function () {
            var on = !el.muted;
            snd.setAttribute('aria-pressed', on ? 'true' : 'false');
            snd.setAttribute('aria-label', on ? 'Togli l\'audio' : 'Attiva l\'audio');
            snd.innerHTML = on
              ? '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12"/></svg>'
              : '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M17 9.5l5 5M22 9.5l-5 5"/></svg>';
          };
          if (soundOn) el.muted = false;
          snd.addEventListener('click', function () {
            el.muted = !el.muted; soundOn = !el.muted;
            if (!el.muted) { el.currentTime = 0; el.play().catch(function () {}); }
            paint();
          });
          paint(); paintSound = paint;
          m.appendChild(snd);
        }
        if (el.play) el.play().catch(function () {
          // il browser non lascia partire il video con l'audio: riparte muto e il tasto torna su «Attiva l'audio»
          if (!el.muted) { el.muted = true; if (paintSound) paintSound(); el.play().catch(function () {}); }
        });
      }
      $('adQ').textContent = '«' + s.question + '»';
      $('adCount').textContent = (list.indexOf(i) + 1) + ' / ' + list.length;
    };
    var step = function (d) {
      var list = visible(), k = list.indexOf(cur);
      show(list[(k + d + list.length) % list.length]);
      dlg.scrollTop = 0;   // la nuova scheda parte dall'inizio; le frecce restano fisse in basso
    };
    z.querySelectorAll('.sign').forEach(function (c) {
      c.addEventListener('click', function () { opener = c; show(+c.dataset.i); dlg.showModal(); });
    });
    $('adPrev').addEventListener('click', function () { step(-1); });
    $('adNext').addEventListener('click', function () { step(1); });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') step(-1);
      if (e.key === 'ArrowRight') step(1);
    });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener('close', function () { $('adMedia').innerHTML = ''; if (opener) opener.focus(); });
    // arrivando da un link come /archetipi-astrologici#scorpione si apre subito quella scheda
    var fromHash = decodeURIComponent((location.hash || '').slice(1)).toLowerCase();
    if (fromHash) arch.signs.forEach(function (s, i) {
      if (s.name.toLowerCase() === fromHash) { opener = z.querySelectorAll('.sign')[i] || null; show(i); dlg.showModal(); }
    });
    // scorrere con il dito sulla scheda: sinistra/destra = archetipo successivo/precedente
    var x0 = null;
    dlg.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    dlg.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1);
    });
  }

  // Home: la scritta di benvenuto resta sempre su una riga: se il carattere non ci sta, si rimpicciolisce quanto basta
  var cap = document.querySelector('.scroll-cap');
  function fitCap() {
    var t = cap && cap.querySelector('span');
    if (!t) return;
    cap.style.fontSize = '';
    var room = cap.clientWidth - Array.prototype.reduce.call(cap.querySelectorAll('.cue'), function (w, c) {
      return w + (c.offsetWidth ? c.offsetWidth + 8 : 0); }, 0) - 8;
    var size = parseFloat(getComputedStyle(cap).fontSize);
    if (t.scrollWidth > room) cap.style.fontSize = Math.floor(size * room / t.scrollWidth * 10) / 10 + 'px';
  }
  if (cap) {
    fitCap();
    addEventListener('resize', fitCap);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitCap);
  }

  // Chi sono: l'albero che cresce dietro "Le mie radici" (solo computer). Parte quando la sezione entra nello schermo,
  // cresce una volta sola e resta fermo sull'ultimo fotogramma. Chi preferisce meno movimento vede solo l'albero finito.
  var rb = document.getElementById('rootsBg');
  if (rb && matchMedia('(min-width:961px)').matches && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var startTree = function () { if (!rb.src) { rb.src = rb.dataset.src; } rb.play().catch(function () {}); };
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { startTree(); io.disconnect(); } });
      }, { threshold: 0.35 });
      io.observe(rb.parentElement);
    } else { startTree(); }
  }

  // Contatti: copia il numero di telefono
  var copy = document.getElementById('copyTel');
  if (copy) {
    copy.addEventListener('click', function (e) {
      var tel = copy.dataset.tel || '';
      if (navigator.clipboard) {
        navigator.clipboard.writeText(tel).then(function () { e.target.textContent = 'Copiato'; });
      }
    });
  }

  // Video della home: chi preferisce meno movimento vede solo l'immagine
  var hv = document.getElementById('heroVideo');
  if (hv && matchMedia('(prefers-reduced-motion: reduce)').matches) { hv.removeAttribute('autoplay'); hv.pause(); }

  // Video della home: audio. I browser bloccano il sonoro automatico,
  // quindi si prova con l'audio e, se bloccato, si attiva al primo tocco nella pagina.
  var sb = document.getElementById('soundToggle');
  if (hv && sb) {
    var showSound = function () {
      var on = !hv.muted;
      sb.setAttribute('aria-pressed', on);
      sb.setAttribute('aria-label', on ? "Disattiva l'audio" : "Attiva l'audio");
    };
    var unmute = function () { hv.muted = false; hv.play().catch(function () {}); showSound(); };
    var onFirstTouch = function (e) {
      if (sb.contains(e.target)) return;
      unmute();
      document.removeEventListener('pointerdown', onFirstTouch);
      document.removeEventListener('keydown', onFirstTouch);
    };
    if (!hv.paused || hv.autoplay) {
      hv.muted = false;
      hv.play().then(showSound).catch(function () {
        hv.muted = true;
        hv.play().catch(function () {});
        showSound();
        document.addEventListener('pointerdown', onFirstTouch);
        document.addEventListener('keydown', onFirstTouch);
      });
    }
    sb.addEventListener('click', function () {
      document.removeEventListener('pointerdown', onFirstTouch);
      document.removeEventListener('keydown', onFirstTouch);
      if (hv.muted) unmute(); else { hv.muted = true; showSound(); }
    });
  }

  // Home, telefono: il pulsante del colloquio si appoggia subito dopo «Abitalo.» (misura la parola reale)
  var abEm = document.querySelector('.hero h1 em'), abWrap = document.querySelector('.h1-wrap');
  if (abEm && abWrap) {
    var fitCta = function () {
      var r = document.createRange(); r.selectNodeContents(abEm);
      var w = r.getBoundingClientRect().width;
      if (w) abWrap.style.setProperty('--abitalo-w', Math.ceil(w) + 'px');
    };
    fitCta();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitCta);
    addEventListener('resize', fitCta);
  }

  // Home: «Il cielo di questo mese». Carta del segno del Sole oggi; «Pesca la tua carta» mescola il mazzo e ne gira una a caso.
  var tSec = document.getElementById('tarot'), tDataEl = document.getElementById('tarotData');
  if (tSec && tDataEl) {
    var CARDS = []; try { CARDS = JSON.parse(tDataEl.textContent); } catch (e) {}
    var ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'];
    var tCard = document.getElementById('tarotCard'), tFace = document.getElementById('tarotFace'), tDeck = document.getElementById('tarotDeck'),
        tQ = document.getElementById('tarotQ'), tHint = document.getElementById('tarotHint'), tKick = document.getElementById('tarotKicker'),
        tDraw = document.getElementById('tarotDraw');
    var esc = function (t) { var d = document.createElement('div'); d.textContent = t; return d.innerHTML; };
    var elSlug = function (e) { return (e || '').toLowerCase(); };
    // dorso delle carte: cornice dorata, ruota dei dodici segni, stella al centro
    var BACK = '<svg viewBox="0 0 200 300" aria-hidden="true" fill="none" stroke="currentColor">' +
      '<rect x="9" y="9" width="182" height="282" rx="8" stroke-width="1.6"/><rect x="15" y="15" width="170" height="270" rx="5" stroke-width=".7"/>' +
      '<circle cx="100" cy="150" r="64" stroke-width="1.2"/><circle cx="100" cy="150" r="47" stroke-width=".7"/><circle cx="100" cy="150" r="22" stroke-width=".7"/>' +
      '<path d="M100 112 L106 144 L138 150 L106 156 L100 188 L94 156 L62 150 L94 144 Z" fill="currentColor" fill-opacity=".85" stroke="none"/>' +
      '<path d="M100 126 L103 147 L124 150 L103 153 L100 174 L97 153 L76 150 L97 147 Z" transform="rotate(45 100 150)" fill="currentColor" fill-opacity=".45" stroke="none"/>' +
      (function () { var g = '', sy = ['♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓'];
        for (var i = 0; i < 12; i++) { var a = (i * 30 - 90) * Math.PI / 180;
          g += '<text x="' + (100 + 55.5 * Math.cos(a)).toFixed(1) + '" y="' + (150 + 55.5 * Math.sin(a) + 4).toFixed(1) + '" font-size="11" text-anchor="middle" fill="currentColor" stroke="none" font-family="serif">' + sy[i] + '︎</text>'; }
        return g; })() +
      '<path d="M100 30 l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4 l10 -4 z M100 242 l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4 l10 -4 z" fill="currentColor" stroke="none"/>' +
      '<path d="M28 28 q14 0 14 14 M172 28 q-14 0 -14 14 M28 272 q14 0 14 -14 M172 272 q-14 0 -14 -14" stroke-width="1"/></svg>';
    tSec.querySelectorAll('.tback').forEach(function (b) { b.innerHTML = BACK; });

    var sunCard = function (d) {      // il segno del Sole oggi (calcolato anche qui, così resta giusto anche se la pagina è in memoria)
      var m = d.getMonth() + 1, g = d.getDate(), best = null;
      CARDS.forEach(function (c) {
        var s = c.start;
        if ((m > s[0] || (m === s[0] && g >= s[1])) && (!best || s[0] > best.start[0] || (s[0] === best.start[0] && s[1] > best.start[1]))) best = c;
      });
      return best || CARDS[9];
    };
    var paint = function (c) {
      var ink = 'ink-' + elSlug(c.el);
      tCard.className = 'tcard' + (tCard.classList.contains('flip') ? ' flip' : '');
      tSec.className = tSec.className.replace(/\bel-\w+/g, '').trim() + ' el-' + elSlug(c.el);
      tCard.href = c.href;
      tCard.setAttribute('aria-label', c.name + ', ' + c.arc + '. Apri questo archetipo');
      tFace.innerHTML = '<div class="tframe"><div class="tnum"><i aria-hidden="true">✦</i>' + ROMAN[c.n - 1] + '<i aria-hidden="true">✦</i></div>' +
        '<div class="tpic">' + (c.fig ? '<img src="' + esc(c.fig) + '" alt="">' : '<span class="twm ' + ink + '" aria-hidden="true">' + c.sym + '</span>') + '</div>' +
        '<div class="tttl"><div class="tarc">' + esc(c.arc) + '</div><div class="tnm">' + c.sym + ' ' + esc(c.name) + ' · <b class="' + ink + '">' + esc(c.el) + '</b></div></div></div>';
      tQ.textContent = '«' + c.q + '»';
    };
    var cur = sunCard(new Date());
    if (CARDS.length) { paint(cur); tKick.innerHTML = 'Il cielo di questo mese · <span class="now">' + esc(cur.name) + '</span>'; }
    // le immagini delle carte, in anticipo, così la carta pescata compare già pronta
    CARDS.forEach(function (c) { if (c.fig) { var im = new Image(); im.src = c.fig; } });

    var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches, busy = false;
    var at = function (ms, f) { setTimeout(f, ms); };
    // il piccolo mazzo nell'apertura: scende alle carte e fa partire la pesca
    var mini = document.getElementById('miniDeck');
    if (mini) mini.addEventListener('click', function (e) {
      e.preventDefault();
      tSec.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      setTimeout(function () { tDraw.click(); }, reduce ? 0 : 750);
    });
    tDraw.addEventListener('click', function () {
      if (busy || !CARDS.length) return; busy = true; tDraw.disabled = true;
      var pool = CARDS.filter(function (c) { return c !== cur; }), next = pool[Math.floor(Math.random() * pool.length)];
      var done = function () {
        cur = next; tKick.innerHTML = 'La tua carta · <span class="now">' + esc(next.name) + '</span>';
        tHint.classList.remove('wait'); tHint.textContent = "Tocca la carta per aprirla, oppure pescane un'altra";
        busy = false; tDraw.disabled = false;
      };
      if (reduce) { paint(next); done(); return; }
      tHint.classList.add('wait'); tHint.textContent = 'Mescolo le carte…'; tQ.classList.add('dim');
      tCard.classList.add('flip');                                                         // la carta si copre
      at(500, function () { tDeck.classList.add('mixing'); tCard.classList.add('out'); });  // il mazzo si mescola, la carta esce a sinistra
      at(1000, function () { tCard.classList.remove('out'); tCard.classList.add('out2'); }); // rientra e riesce a destra
      at(1500, function () { tCard.classList.remove('out2'); tHint.textContent = 'Respira…'; });
      at(1900, function () { tCard.classList.add('out'); });                                 // un ultimo passaggio, sempre coperta
      at(2350, function () { tCard.classList.remove('out'); paint(next); });
      at(2750, function () { tDeck.classList.remove('mixing'); tHint.textContent = 'Ecco la tua carta'; });
      at(3000, function () { tCard.classList.remove('flip'); tCard.classList.add('glow'); });  // si gira e si illumina
      at(3400, function () { tQ.classList.remove('dim'); });
      at(3900, function () { tCard.classList.remove('glow'); done(); });
    });
  }
})();
