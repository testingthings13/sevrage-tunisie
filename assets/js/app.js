/* Clinique Espoir — El Menzah 9
   Three behaviours only: the drawer, the tile-set reveal, the contact form. */
(function () {
  'use strict';
  var root = document.documentElement;
  root.classList.add('js');

  /* ── Mobile drawer ───────────────────────────────────────── */
  var burger = document.querySelector('.burger');
  var drawer = document.getElementById('nav-mobile');

  function closeDrawer() {
    if (!drawer) return;
    drawer.hidden = true;
    burger.setAttribute('aria-expanded', 'false');
    burger.querySelector('.visually-hidden').textContent = 'Ouvrir le menu';
  }

  if (burger && drawer) {
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      if (open) { closeDrawer(); return; }
      drawer.hidden = false;
      burger.setAttribute('aria-expanded', 'true');
      burger.querySelector('.visually-hidden').textContent = 'Fermer le menu';
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') closeDrawer();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeDrawer();
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 1060) closeDrawer();
    });
  }

  /* ── The tile sets: one authored reveal, staggered per row ─ */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* Section furniture reveals too, without cluttering the markup. */
  document.querySelectorAll('.section__head, .split__text, .sevrage__aside, .venue__text')
    .forEach(function (el) { el.classList.add('reveal'); });
  document.querySelectorAll('.faq details')
    .forEach(function (el) { el.classList.add('reveal'); });
  document.querySelectorAll('.split__text, .sevrage__aside, .venue__text')
    .forEach(function (el) { el.classList.add('reveal--left'); });
  document.querySelectorAll('.pairs, .signs, .day, .path')
    .forEach(function (el) { el.classList.add('reveal', 'reveal--right'); });
  document.querySelectorAll('.compare, .warn')
    .forEach(function (el) { el.classList.add('reveal--zoom'); });

  var targets = Array.prototype.slice.call(document.querySelectorAll('.reveal'));

  function setAll() {
    targets.forEach(function (el) { el.classList.add('is-set'); });
  }

  if (reduce.matches) {
    setAll();
  } else {
    /* Plain geometry, checked on scroll: no observer to miss a frame,
       and a hard fail-safe so a reveal can never keep content hidden. */
    var pending = targets.slice();

    var sweep = function () {
      if (!pending.length) return;
      var h = window.innerHeight;
      var due = [];
      pending = pending.filter(function (el) {
        if (el.getBoundingClientRect().top < h * 0.92) { due.push(el); return false; }
        return true;
      });
      due.forEach(function (el, i) {
        el.style.setProperty('--d', Math.min(i, 6) * 70 + 'ms');
        el.classList.add('is-set');
      });
    };

    window.addEventListener('scroll', sweep, { passive: true });
    window.addEventListener('resize', sweep);
    window.addEventListener('load', sweep);
    sweep();
    window.setTimeout(sweep, 200);
    window.setTimeout(setAll, 4000);   /* fail-safe: nothing stays invisible */
  }

  /* ── Masthead: condenses once you leave the first viewport ─ */
  var masthead = document.querySelector('.masthead');
  if (masthead) {
    var stuck = false;
    var onScroll = function () {
      var should = window.scrollY > 24;
      if (should !== stuck) {
        stuck = should;
        masthead.classList.toggle('is-stuck', stuck);
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── Hero photograph drifts a little slower than the page ── */
  var heroImg = document.querySelector('.hero__figure');
  if (heroImg && !reduce.matches) {
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        var y = window.scrollY;
        if (y < window.innerHeight * 1.2) {
          heroImg.style.transform = 'translate3d(0,' + (y * 0.06).toFixed(1) + 'px,0)';
        }
        ticking = false;
      });
    }, { passive: true });
  }

  /* ── Headline, word by word ──────────────────────────────── */
  var headline = document.querySelector('.display');
  if (headline && !reduce.matches) {
    var i = 0;
    headline.querySelectorAll('em, br').forEach(function () {});
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (child) {
        if (child.nodeType === 3 && child.textContent.trim()) {
          var frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part.trim()) { frag.appendChild(document.createTextNode(part)); return; }
            var s = document.createElement('span');
            s.className = 'w';
            s.style.setProperty('--i', i++);
            s.textContent = part;
            frag.appendChild(s);
          });
          child.parentNode.replaceChild(frag, child);
        } else if (child.nodeType === 1) {
          walk(child);
        }
      });
    };
    walk(headline);
  }

  /* ── Scroll progress ─────────────────────────────────────── */
  var bar = document.querySelector('.progress i');
  if (bar) {
    var barTick = false;
    var drawBar = function () {
      if (barTick) return;
      barTick = true;
      window.requestAnimationFrame(function () {
        var max = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.setProperty('--p', max > 0 ? Math.min(1, window.scrollY / max).toFixed(4) : 0);
        barTick = false;
      });
    };
    window.addEventListener('scroll', drawBar, { passive: true });
    window.addEventListener('resize', drawBar);
    drawBar();
  }

  /* ── The sevrage path draws itself as you pass it ─────────── */
  var path = document.querySelector('.path');
  if (path && !reduce.matches) {
    var pathTick = false;
    var drawPath = function () {
      if (pathTick) return;
      pathTick = true;
      window.requestAnimationFrame(function () {
        var r = path.getBoundingClientRect();
        var anchor = window.innerHeight * 0.62;
        var ratio = (anchor - r.top) / r.height;
        path.style.setProperty('--draw', Math.max(0, Math.min(1, ratio)).toFixed(4));
        pathTick = false;
      });
    };
    window.addEventListener('scroll', drawPath, { passive: true });
    window.addEventListener('resize', drawPath);
    drawPath();
  }

  /* ── Avant / après: drag to compare ──────────────────────── */
  var compare = document.querySelector('.compare');
  if (compare) {
    var range = compare.querySelector('.compare__range');
    var setX = function () { compare.style.setProperty('--x', range.value + '%'); };
    range.addEventListener('input', setX);
    setX();

    /* Pointer anywhere on the image moves the handle, not just the thumb. */
    var track = function (e) {
      var r = compare.getBoundingClientRect();
      var pct = ((e.clientX - r.left) / r.width) * 100;
      range.value = Math.max(0, Math.min(100, pct));
      setX();
    };
    var dragging = false;
    compare.addEventListener('pointerdown', function (e) {
      if (e.target.closest('figcaption')) return;
      dragging = true; compare.setPointerCapture(e.pointerId); track(e);
    });
    compare.addEventListener('pointermove', function (e) { if (dragging) track(e); });
    compare.addEventListener('pointerup', function () { dragging = false; });
    compare.addEventListener('pointercancel', function () { dragging = false; });

    /* An unprompted first sweep, so the control announces itself. */
    if (!reduce.matches) {
      var swept = false;
      var sweepOnce = function () {
        if (swept) return;
        var r = compare.getBoundingClientRect();
        if (r.top > window.innerHeight * 0.75 || r.bottom < 0) return;
        swept = true;
        window.removeEventListener('scroll', sweepOnce);
        var t0 = null, from = parseFloat(range.value);
        var step = function (t) {
          if (t0 === null) t0 = t;
          var k = Math.min(1, (t - t0) / 1600);
          var e = 1 - Math.pow(1 - k, 3);
          /* sweeps left, uncovering the sixth week, then settles back */
          var v = from + (14 - from) * Math.sin(e * Math.PI);
          range.value = v; setX();
          if (k < 1) window.requestAnimationFrame(step);
        };
        window.requestAnimationFrame(step);
      };
      window.addEventListener('scroll', sweepOnce, { passive: true });
      sweepOnce();
    }
  }

  /* ── Slow drift on the venue photographs ─────────────────── */
  var floaters = Array.prototype.slice.call(document.querySelectorAll('.venue__pics img'));
  if (floaters.length && !reduce.matches) {
    var fTick = false;
    var floatOn = function () {
      if (fTick) return;
      fTick = true;
      window.requestAnimationFrame(function () {
        var mid = window.innerHeight / 2;
        floaters.forEach(function (el, i) {
          var r = el.getBoundingClientRect();
          if (r.bottom < 0 || r.top > window.innerHeight) return;
          var d = (r.top + r.height / 2 - mid) / window.innerHeight;
          el.style.transform = 'translate3d(0,' + (d * (10 + i * 8)).toFixed(1) + 'px,0) scale(1.06)';
        });
        fTick = false;
      });
    };
    window.addEventListener('scroll', floatOn, { passive: true });
    floatOn();
  }

  /* ── La barre d'appel s'efface devant le formulaire ──────── */
  var callbar = document.querySelector('.callbar');
  var contactSection = document.getElementById('contact');
  if (callbar && contactSection) {
    var barTick2 = false;
    var checkBar = function () {
      if (barTick2) return;
      barTick2 = true;
      window.requestAnimationFrame(function () {
        var r = contactSection.getBoundingClientRect();
        callbar.dataset.hidden = (r.top < window.innerHeight * 0.85) ? 'true' : 'false';
        barTick2 = false;
      });
    };
    window.addEventListener('scroll', checkBar, { passive: true });
    window.addEventListener('resize', checkBar);
    checkBar();
  }

  /* ── Six semaines : une scène qui se transforme ──────────── */
  var weeks = document.querySelector('.weeks');
  if (weeks) {
    var BARS = [
      [.18, .62, .12, .95, .22, .08, .72, .14, .38, .10, .52, .18, .06, .42],
      [.30, .66, .25, .92, .35, .20, .74, .30, .45, .24, .58, .32, .20, .50],
      [.45, .70, .42, .88, .50, .38, .76, .46, .55, .42, .64, .48, .40, .58],
      [.58, .74, .56, .86, .62, .54, .78, .60, .66, .56, .70, .60, .55, .66],
      [.68, .78, .70, .84, .72, .68, .80, .72, .74, .70, .76, .72, .70, .74],
      [.78, .82, .80, .86, .80, .79, .84, .80, .82, .80, .83, .81, .80, .82],
      [.86, .88, .87, .90, .88, .87, .89, .88, .88, .87, .89, .88, .87, .88]
    ];
    var TIMES = [[3, 0], [4, 30], [5, 30], [6, 15], [6, 45], [7, 15], [7, 30]];
    var RAMP = [
      ['#10222F', '#F5F7F6'],   // fond
      ['#0A1620', '#DCE8F2'],   // ciel
      ['#33546B', '#2B4B9B'],   // cadre
      ['#22384A', '#C6D0CD'],   // traits
      ['#5C7183', '#2B4B9B'],   // silhouette
      ['#8EACC6', '#2B4B9B']    // horloge
    ];
    var VARS = ['--sc-bg', '--sc-sky', '--sc-frame', '--sc-line', '--sc-ink', '--sc-clock'];

    var hex = function (c) {
      return [parseInt(c.substr(1, 2), 16), parseInt(c.substr(3, 2), 16), parseInt(c.substr(5, 2), 16)];
    };
    var mix = function (a, b, t) {
      var x = hex(a), y = hex(b);
      return 'rgb(' + x.map(function (v, i) { return Math.round(v + (y[i] - v) * t); }).join(',') + ')';
    };

    var bars = weeks.querySelectorAll('.sc-bars rect');
    var texts = weeks.querySelectorAll('.weeks__t');
    var list = weeks.querySelector('.weeks__texts');
    var timeEl = document.getElementById('wk-time');
    var stepBtns = document.querySelectorAll('.weeks__steps button');
    var playBtn = document.querySelector('.weeks__play');
    var playTxt = playBtn && playBtn.querySelector('.weeks__play-t');
    var isFr = document.documentElement.lang === 'fr';
    var current = 0, timer = null;

    if (list) list.classList.add('is-live');

    function show(i) {
      current = i;
      var t = i / 6;

      VARS.forEach(function (name, k) {
        weeks.style.setProperty(name, mix(RAMP[k][0], RAMP[k][1], t));
      });
      weeks.style.setProperty('--a', String(Math.max(0, 1 - i / 3.2)));
      weeks.style.setProperty('--b', String(Math.min(1, Math.max(0, (i - 2) / 2.4))));
      weeks.style.setProperty('--plant', String(Math.min(1, Math.max(0, (i - 3) / 2))));

      BARS[i].forEach(function (h, k) { if (bars[k]) bars[k].style.setProperty('--h', String(h)); });

      var hh = TIMES[i][0], mm = TIMES[i][1];
      weeks.style.setProperty('--hr', ((hh % 12) * 30 + mm * 0.5) + 'deg');
      weeks.style.setProperty('--mr', (mm * 6) + 'deg');
      if (timeEl) {
        var p = (mm < 10 ? '0' : '') + mm;
        timeEl.textContent = isFr ? ('0' + hh).slice(-2) + ' h ' + p : ('0' + hh).slice(-2) + ':' + p;
      }

      texts.forEach(function (el) { el.classList.toggle('is-on', +el.dataset.week === i); });
      stepBtns.forEach(function (b) { b.setAttribute('aria-pressed', String(+b.dataset.go === i)); });
    }

    function stop() {
      if (!timer) return;
      window.clearInterval(timer);
      timer = null;
      if (playTxt) playTxt.textContent = playTxt.dataset.play;
    }

    stepBtns.forEach(function (b) {
      b.addEventListener('click', function () { stop(); show(+b.dataset.go); });
    });

    if (playBtn && playTxt) {
      playTxt.dataset.play = playTxt.textContent;
      playBtn.addEventListener('click', function () {
        if (timer) { stop(); return; }
        playTxt.textContent = playTxt.dataset.stop || playTxt.textContent;
        show(0);
        timer = window.setInterval(function () {
          if (current >= 6) { stop(); return; }
          show(current + 1);
        }, 2100);
      });
    }

    show(0);

    /* la scène se lance seule quand on arrive dessus, une seule fois */
    if (!reduce.matches) {
      var started = false;
      var autostart = function () {
        if (started) return;
        var r = weeks.getBoundingClientRect();
        if (r.top > window.innerHeight * 0.6 || r.bottom < 0) return;
        started = true;
        window.removeEventListener('scroll', autostart);
        if (playBtn) playBtn.click();
      };
      window.addEventListener('scroll', autostart, { passive: true });
      autostart();
    }
  }

  /* ── Sortie rapide ───────────────────────────────────────── */
  var quick = document.querySelector('.quickexit');
  var leave = function () {
    try { window.location.replace('https://www.google.com'); }
    catch (e) { window.location.href = 'https://www.google.com'; }
  };
  if (quick) {
    quick.addEventListener('click', leave);
    var escCount = 0, escTimer = null;
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      escCount++;
      window.clearTimeout(escTimer);
      escTimer = window.setTimeout(function () { escCount = 0; }, 700);
      if (escCount >= 2) leave();
    });
  }

  /* ── Page de remerciement : cas où l'e-mail n'est pas parti ─ */
  var alerte = document.getElementById('merci-alerte');
  if (alerte && /[?&]envoi=differe/.test(window.location.search)) {
    alerte.dataset.state = 'err';
    alerte.textContent = 'Votre demande a bien été enregistrée, mais notre serveur d\u2019e-mail '
      + 'n\u2019a pas répondu. Si vous n\u2019avez pas de retour d\u2019ici deux heures, appelez le +216 00 000 000.';
  }

  /* ── Formulaires : on valide, le serveur envoie ──────────── */
  Array.prototype.forEach.call(document.querySelectorAll('form[action="envoi.php"]'), function (form) {
    var status = form.querySelector('.form__status');

    form.addEventListener('submit', function (e) {
      var nom = form.nom, tel = form.tel, consent = form.consent;

      [nom, tel].forEach(function (f) { if (f) f.classList.remove('invalid'); });

      function stop(msg, field) {
        e.preventDefault();
        if (status) { status.dataset.state = 'err'; status.textContent = msg; }
        if (field) { field.classList.add('invalid'); field.focus(); }
      }

      if (nom && !nom.value.trim()) {
        return stop('Indiquez votre nom, pour que nous sachions qui rappeler.', nom);
      }
      if (tel && !tel.value.trim()) {
        return stop('Un numéro de téléphone est nécessaire : c\u2019est par là que nous répondons.', tel);
      }
      if (consent && !consent.checked) {
        return stop('Cochez la case pour que nous puissions vous recontacter.', consent);
      }

      if (status) { status.dataset.state = 'ok'; status.textContent = 'Envoi en cours…'; }
      var btn = form.querySelector('button[type="submit"]');
      if (btn) { btn.disabled = true; }
    });
  });

  /* ── Active section in the nav ───────────────────────────── */
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav a[href^="#"]'));
  var sections = links
    .map(function (a) { return document.querySelector(a.getAttribute('href')); })
    .filter(Boolean);

  if (sections.length && 'IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) {
          a.style.color = a.getAttribute('href') === '#' + en.target.id ? 'var(--ink)' : '';
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { spy.observe(s); });
  }
})();

/* ── Enhanced Animations Setup ──────────────────────────── */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* Services & Features: Add reveal class for scroll animations */
  document.querySelectorAll('.service, .service__features li, .section__title, details')
    .forEach(function (el) { 
      if (!el.classList.contains('reveal')) {
        el.classList.add('reveal');
      }
    });

  /* Emergency Button Pulse Animation */
  var emergencyBtn = document.querySelector('.callbar .btn--call');
  if (emergencyBtn && !reduce.matches) {
    emergencyBtn.classList.add('btn--call-urgent');
  }

  /* Enhanced Form State Feedback */
  Array.prototype.forEach.call(document.querySelectorAll('form[action="envoi.php"]'), function (form) {
    var originalSubmit = form.onsubmit;
    var status = form.querySelector('.form__status');

    form.addEventListener('submit', function (e) {
      if (status && !form.classList.contains('submitted')) {
        form.classList.add('submitted');
        setTimeout(function () {
          if (status.dataset.state === 'ok') {
            setTimeout(function () {
              form.classList.remove('submitted');
            }, 2000);
          }
        }, 3000);
      }
    });
  });

  /* Parallax Effect on Hero Section */
  var hero = document.querySelector('.hero');
  if (hero && !reduce.matches) {
    var updateParallax = function () {
      var scrollPos = window.scrollY;
      hero.style.backgroundPosition = '0 ' + (scrollPos * 0.5) + 'px';
    };
    window.addEventListener('scroll', updateParallax, { passive: true });
  }

  /* Scroll reveal trigger for new elements */
  var targets = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
  if (targets.length && !reduce.matches) {
    var pending = targets.filter(function (el) { 
      return !el.classList.contains('is-set'); 
    });

    var sweep = function () {
      if (!pending.length) return;
      var h = window.innerHeight;
      var due = [];
      pending = pending.filter(function (el) {
        if (el.getBoundingClientRect().top < h * 0.92) { due.push(el); return false; }
        return true;
      });
      due.forEach(function (el, i) {
        el.style.setProperty('--d', Math.min(i, 6) * 70 + 'ms');
        el.classList.add('is-set');
      });
    };

    window.addEventListener('scroll', sweep, { passive: true });
    window.addEventListener('resize', sweep);
    window.addEventListener('load', sweep);
    sweep();
    window.setTimeout(sweep, 200);
    window.setTimeout(function () {
      pending.forEach(function (el) { el.classList.add('is-set'); });
    }, 4000);
  }
})();
