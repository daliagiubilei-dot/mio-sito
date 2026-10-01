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
})();
