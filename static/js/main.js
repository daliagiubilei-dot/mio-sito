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

  // Archetipi: filtro per elemento
  var z = document.getElementById('zodiac');
  document.querySelectorAll('.filters button').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.filters button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      if (z) z.querySelectorAll('.sign').forEach(function (c) { c.hidden = !(b.dataset.el === 'tutti' || c.dataset.el === b.dataset.el); });
    });
  });

  // Archetipi: la carta con personaggio apre video e immagini; chiudendo, i video si fermano
  document.querySelectorAll('.sign-open').forEach(function (b) {
    var d = document.getElementById(b.dataset.dialog);
    if (!d || !d.showModal) return;
    b.addEventListener('click', function () { d.showModal(); });
    d.querySelector('.arch-close').addEventListener('click', function () { d.close(); });
    d.addEventListener('click', function (e) { if (e.target === d) d.close(); });
    d.addEventListener('close', function () { d.querySelectorAll('video').forEach(function (v) { v.pause(); }); b.focus(); });
  });

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
})();
