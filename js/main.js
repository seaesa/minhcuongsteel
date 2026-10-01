(function () {
  'use strict';

  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };
  var isSmall = function () { return window.innerWidth < 550; };

  /* ------------------------------------------------------------------
     Sticky header + back to top
     ------------------------------------------------------------------ */
  var headerWrapper = $('#headerWrapper');
  var topLink = $('#top-link');
  var STICK_AT = 200;
  function onScroll() {
    var y = window.pageYOffset;
    if (y > STICK_AT) headerWrapper.classList.add('stuck');
    else headerWrapper.classList.remove('stuck');
    topLink.classList.toggle('active', y > 300);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  topLink.addEventListener('click', function (e) {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  /* ------------------------------------------------------------------
     Popups (mobile menu / search / video) – magnific style
     ------------------------------------------------------------------ */
  var openPopup = null;
  function showPopup(bg, wrap, onClose) {
    closePopup();
    bg.classList.add('ready');
    wrap.classList.add('ready');
    wrap.setAttribute('aria-hidden', 'false');
    document.body.classList.add('lock');
    openPopup = { bg: bg, wrap: wrap, onClose: onClose };
  }
  function closePopup() {
    if (!openPopup) return;
    var p = openPopup;
    openPopup = null;
    p.bg.classList.remove('ready');
    p.wrap.classList.remove('ready');
    p.wrap.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('lock');
    if (p.onClose) p.onClose();
  }
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closePopup(); });

  // mobile menu
  var menuBg = $('#menuBg'), menuWrap = $('#menuWrap');
  $('#menuOpen').addEventListener('click', function () { showPopup(menuBg, menuWrap); });
  $('#menuClose').addEventListener('click', closePopup);
  menuWrap.addEventListener('click', function (e) { if (e.target === menuWrap) closePopup(); });
  menuBg.addEventListener('click', closePopup);
  $$('.nav-sidebar .toggle').forEach(function (btn) {
    btn.addEventListener('click', function () { btn.parentNode.classList.toggle('active'); });
  });
  window.addEventListener('resize', function () {
    if (openPopup && openPopup.wrap === menuWrap && window.innerWidth >= 850) closePopup();
  });

  // search
  var searchBg = $('#searchBg'), searchWrap = $('#searchWrap');
  $$('[data-search]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      showPopup(searchBg, searchWrap);
      setTimeout(function () { $('.search-field', searchWrap).focus(); }, 300);
    });
  });
  searchWrap.addEventListener('click', function (e) { if (e.target === searchWrap) closePopup(); });
  $('[data-close]', searchWrap).addEventListener('click', closePopup);

  // video
  var videoBg = $('#videoBg'), videoWrap = $('#videoWrap'), videoFrame = $('#videoFrame');
  $$('[data-video]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      videoFrame.innerHTML = '<iframe src="https://www.youtube.com/embed/' + a.getAttribute('data-video') +
        '?autoplay=1&rel=0" allow="autoplay; encrypted-media; fullscreen" allowfullscreen></iframe>';
      showPopup(videoBg, videoWrap, function () { videoFrame.innerHTML = ''; });
    });
  });
  videoWrap.addEventListener('click', function (e) { if (e.target === videoWrap) closePopup(); });
  $('[data-close]', videoWrap).addEventListener('click', closePopup);

  /* ------------------------------------------------------------------
     Language switcher (Google Translate, like GTranslate plugin)
     ------------------------------------------------------------------ */
  function currentLang() {
    var m = document.cookie.match(/googtrans=\/vi\/([^;]+)/);
    return m ? decodeURIComponent(m[1]) : 'vi';
  }
  function setLang(lang) {
    var host = location.hostname;
    var expire = lang === 'vi' ? '; expires=Thu, 01 Jan 1970 00:00:00 GMT' : '';
    var value = 'googtrans=/vi/' + lang + expire + '; path=/';
    document.cookie = value;
    if (host && host.indexOf('.') > -1) document.cookie = value + '; domain=' + host;
    location.reload();
  }
  var lang = currentLang();
  $$('.gt-switcher').forEach(function (sw) {
    var sel = $('.gt-selected img', sw);
    sel.src = 'images/flags/' + lang + '.svg';
    sel.alt = lang;
    $$('.gt-options a', sw).forEach(function (a) {
      a.classList.toggle('gt-current', a.getAttribute('data-lang') === lang);
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var l = a.getAttribute('data-lang');
        if (l !== lang) setLang(l);
      });
    });
    $('.gt-selected', sw).addEventListener('click', function (e) {
      e.stopPropagation();
      sw.classList.toggle('open');
    });
  });
  document.addEventListener('click', function () {
    $$('.gt-switcher.open').forEach(function (sw) { sw.classList.remove('open'); });
  });
  if (lang !== 'vi') {
    var gtDiv = document.createElement('div');
    gtDiv.id = 'google_translate_element';
    gtDiv.style.display = 'none';
    document.body.appendChild(gtDiv);
    window.googleTranslateElementInit = function () {
      /* global google */
      new google.translate.TranslateElement({ pageLanguage: 'vi', autoDisplay: false }, 'google_translate_element');
    };
    var s = document.createElement('script');
    s.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    document.body.appendChild(s);
    var st = document.createElement('style');
    st.textContent = '.skiptranslate iframe,.goog-te-banner-frame{display:none!important}body{top:0!important}';
    document.head.appendChild(st);
  }

  /* ------------------------------------------------------------------
     Scroll reveal ([data-animate])
     ------------------------------------------------------------------ */
  var revealEls = $$('[data-animate], [data-reveal]').filter(function (el) { return !el.closest('.hero-slide'); });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          if (en.target.hasAttribute('data-reveal')) en.target.classList.add('is-revealed');
          else en.target.setAttribute('data-animated', 'true');
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -5% 0px', threshold: 0 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.setAttribute('data-animated', 'true'); el.classList.add('is-revealed'); });
  }

  /* ------------------------------------------------------------------
     Count-up (29 years)
     ------------------------------------------------------------------ */
  var counters = $$('.count-up');
  function runCount(el) {
    var to = parseInt(el.getAttribute('data-to'), 10) || 0;
    var start = null, dur = 2000;
    el.classList.add('active');
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    }
    el.textContent = '0';
    requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { runCount(en.target); cio.unobserve(en.target); }
      });
    }, { threshold: .5 });
    counters.forEach(function (c) { cio.observe(c); });
  } else {
    counters.forEach(function (c) { c.classList.add('active'); });
  }

  /* ------------------------------------------------------------------
     Drag helper
     ------------------------------------------------------------------ */
  function attachDrag(area, handlers) {
    var startX = 0, startY = 0, dx = 0, down = false, dragging = false, moved = false;
    area.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      down = true; dragging = false; moved = false; dx = 0;
      startX = e.clientX; startY = e.clientY;
    });
    window.addEventListener('pointermove', function (e) {
      if (!down) return;
      var mx = e.clientX - startX, my = e.clientY - startY;
      if (!dragging) {
        if (Math.abs(mx) < 10) { if (Math.abs(my) > 10) down = false; return; }
        dragging = true;
        area.classList.add('dragging');
        handlers.start();
      }
      dx = mx; moved = true;
      handlers.move(dx);
    });
    function end() {
      if (!down) return;
      down = false;
      if (dragging) { area.classList.remove('dragging'); handlers.end(dx); }
      dragging = false;
    }
    window.addEventListener('pointerup', end);
    window.addEventListener('pointercancel', end);
    area.addEventListener('click', function (e) { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
    area.addEventListener('dragstart', function (e) { e.preventDefault(); });
  }

  /* ------------------------------------------------------------------
     Flickity-like slider (hero, news, partners)
     options: autoPlay(ms|0), pauseOnHover, group(fn -> cells per page), onSelect
     ------------------------------------------------------------------ */
  function Slider(root, opts) {
    this.root = root;
    this.opts = opts;
    this.viewport = $('.slider-viewport', root);
    this.track = $('.slider-track', root);
    this.cells = Array.prototype.slice.call(this.track.children);
    this.dots = $('.slider-dots', root);
    this.index = 0;
    this.timer = null;
    this.paused = false;
    this.build();
    var self = this;
    window.addEventListener('resize', function () { self.layout(); });
    if (opts.pauseOnHover) {
      root.addEventListener('mouseenter', function () { self.paused = true; });
      root.addEventListener('mouseleave', function () { self.paused = false; });
    }
    var prev = $('.slider-arrow.prev', root), next = $('.slider-arrow.next', root);
    if (prev) prev.addEventListener('click', function () { self.go(self.index - 1); self.restart(); });
    if (next) next.addEventListener('click', function () { self.go(self.index + 1); self.restart(); });
    attachDrag(this.viewport, {
      start: function () { self.stop(); self.track.classList.remove('animate'); },
      move: function (dx) { self.setX(self.baseX() + dx); },
      end: function (dx) {
        var w = self.pageWidth();
        var steps = Math.abs(dx) > w / 4 ? Math.max(1, Math.round(Math.abs(dx) / w)) : (Math.abs(dx) > 10 ? 1 : 0);
        self.go(self.index + (dx < 0 ? steps : -steps));
        self.restart();
      }
    });
    this.restart();
  }
  Slider.prototype.perPage = function () { return this.opts.group ? this.opts.group() : 1; };
  Slider.prototype.pages = function () { return Math.ceil(this.cells.length / this.perPage()); };
  Slider.prototype.cellWidth = function () { return this.cells[0].getBoundingClientRect().width; };
  Slider.prototype.pageWidth = function () { return this.cellWidth() * this.perPage(); };
  Slider.prototype.build = function () {
    var self = this;
    // clones before and after for seamless wrap
    this.track.querySelectorAll('.is-clone').forEach(function (c) { c.remove(); });
    var before = document.createDocumentFragment(), after = document.createDocumentFragment();
    this.cells.forEach(function (c) {
      var a = c.cloneNode(true); a.classList.add('is-clone'); a.classList.remove('is-selected'); a.setAttribute('aria-hidden', 'true'); after.appendChild(a);
      var b = c.cloneNode(true); b.classList.add('is-clone'); b.classList.remove('is-selected'); b.setAttribute('aria-hidden', 'true'); before.appendChild(b);
    });
    this.track.insertBefore(before, this.track.firstChild);
    this.track.appendChild(after);
    this.renderDots();
    this.layout();
  };
  Slider.prototype.renderDots = function () {
    if (!this.dots) return;
    var self = this, n = this.pages();
    this.dots.innerHTML = '';
    for (var i = 0; i < n; i++) {
      var li = document.createElement('li');
      li.setAttribute('aria-label', 'Page dot ' + (i + 1));
      (function (k) { li.addEventListener('click', function () { self.go(k); self.restart(); }); })(i);
      this.dots.appendChild(li);
    }
    this.updateDots();
  };
  Slider.prototype.updateDots = function () {
    if (!this.dots) return;
    var p = ((this.index % this.pages()) + this.pages()) % this.pages();
    Array.prototype.forEach.call(this.dots.children, function (d, i) { d.classList.toggle('is-selected', i === p); });
  };
  Slider.prototype.baseX = function () { return -(this.cells.length + this.index * this.perPage()) * this.cellWidth(); };
  Slider.prototype.setX = function (x) { this.track.style.transform = 'translate3d(' + x + 'px,0,0)'; };
  Slider.prototype.layout = function () {
    if (this.dots && this.dots.children.length !== this.pages()) { this.index = 0; this.renderDots(); }
    this.track.classList.remove('animate');
    this.setX(this.baseX());
  };
  Slider.prototype.go = function (i) {
    var self = this, n = this.pages();
    this.index = i;
    this.track.classList.add('animate');
    this.setX(this.baseX());
    var real = ((i % n) + n) % n;
    this.updateDotsTo(real);
    if (this.opts.onSelect) this.opts.onSelect(real, this);
    clearTimeout(this.snapTimer);
    this.snapTimer = setTimeout(function () {
      if (self.index !== real) {
        self.index = real;
        self.track.classList.remove('animate');
        self.setX(self.baseX());
      }
    }, 460);
  };
  Slider.prototype.updateDotsTo = function (real) {
    if (!this.dots) return;
    Array.prototype.forEach.call(this.dots.children, function (d, k) { d.classList.toggle('is-selected', k === real); });
  };
  Slider.prototype.stop = function () { clearInterval(this.timer); };
  Slider.prototype.restart = function () {
    var self = this;
    this.stop();
    if (!this.opts.autoPlay) return;
    this.timer = setInterval(function () {
      if (self.paused || document.hidden || !self.root.offsetParent) return;
      self.go(self.index + 1);
    }, this.opts.autoPlay);
  };

  // hero sliders (desktop + mobile variants)
  $$('[data-slider="hero"]').forEach(function (root) {
    var real = $$('.hero-slide', root);
    function loadBg(slide) {
      var bg = slide.getAttribute('data-bg');
      if (bg && !slide.style.backgroundImage) slide.style.backgroundImage = 'url(' + bg + ')';
    }
    function select(i) {
      var all = $$('.hero-slide', root);
      real.forEach(function (s, k) { s.classList.toggle('is-selected', k === i); });
      all.forEach(function (s) {
        var col = $('[data-animate]', s);
        if (!col) return;
        if (s === real[i]) {
          loadBg(s);
          col.setAttribute('data-animated', 'false');
          void col.offsetWidth;
          col.setAttribute('data-animated', 'true');
        } else if (!s.classList.contains('is-clone')) {
          col.setAttribute('data-animated', 'false');
        }
      });
      loadBg(real[(i + 1) % real.length]);
    }
    new Slider(root, { autoPlay: 6000, pauseOnHover: true, onSelect: select });
    // clones: always show content + preload neighbours
    $$('.hero-slide.is-clone', root).forEach(function (c) {
      var col = $('[data-animate]', c); if (col) col.setAttribute('data-animated', 'true');
      loadBg(c);
    });
    setTimeout(function () { select(0); }, 50);
  });

  // news slider (medium/small)
  $$('[data-slider="news"]').forEach(function (root) {
    new Slider(root, { autoPlay: 2000, pauseOnHover: true });
  });

  // partners
  $$('[data-slider="partners"]').forEach(function (root) {
    new Slider(root, { autoPlay: 0, group: function () { return isSmall() ? 3 : 4; } });
  });

  /* ------------------------------------------------------------------
     Projects – slick centre mode (autoplay 2s, speed 500)
     ------------------------------------------------------------------ */
  function CenterSlider(root) {
    this.root = root;
    this.list = $('.slick-list', root);
    this.track = $('.slick-track', root);
    this.slides = Array.prototype.slice.call(this.track.children);
    this.n = this.slides.length;
    this.clones = 3;
    this.cur = 0;
    this.paused = false;
    var self = this;
    var before = document.createDocumentFragment(), after = document.createDocumentFragment();
    this.slides.slice(-this.clones).forEach(function (s) { var c = s.cloneNode(true); c.classList.add('is-clone'); before.appendChild(c); });
    this.slides.slice(0, this.clones).forEach(function (s) { var c = s.cloneNode(true); c.classList.add('is-clone'); after.appendChild(c); });
    this.track.insertBefore(before, this.track.firstChild);
    this.track.appendChild(after);
    this.all = Array.prototype.slice.call(this.track.children);
    root.addEventListener('mouseenter', function () { self.paused = true; });
    root.addEventListener('mouseleave', function () { self.paused = false; });
    window.addEventListener('resize', function () { self.layout(); });
    attachDrag(this.list, {
      start: function () { self.stop(); self.track.classList.remove('animate'); },
      move: function (dx) { self.setX(self.baseX() + dx); },
      end: function (dx) { self.go(self.cur + (dx < 0 ? 1 : -1)); self.start(); }
    });
    var panel = root.closest('.panel');
    this.panel = panel;
    var prevBtn = $('.proj-nav.prev', panel), nextBtn = $('.proj-nav.next', panel);
    if (prevBtn) prevBtn.addEventListener('click', function () { self.go(self.cur - 1); self.start(); });
    if (nextBtn) nextBtn.addEventListener('click', function () { self.go(self.cur + 1); self.start(); });
    [prevBtn, nextBtn].forEach(function (b) {
      if (!b) return;
      b.addEventListener('mouseenter', function () { self.paused = true; });
      b.addEventListener('mouseleave', function () { self.paused = false; });
    });
    this.layout();
    this.start();
  }
  CenterSlider.prototype.alignNav = function () {
    var cur = this.track.querySelector('.project-slide.is-current .project-image');
    if (!cur || !this.panel.offsetParent) return;
    var img = cur.getBoundingClientRect(), p = this.panel.getBoundingClientRect();
    this.panel.style.setProperty('--nav-top', Math.round(img.top + img.height / 2 - p.top) + 'px');
  };
  CenterSlider.prototype.show = function () { return isSmall() ? 1 : 3; };
  CenterSlider.prototype.width = function () {
    var cs = getComputedStyle(this.list);
    var inner = this.list.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    return inner / this.show();
  };
  CenterSlider.prototype.baseX = function () {
    var offset = this.show() === 3 ? 1 : 0;
    return -((this.cur + this.clones - offset) * this.w);
  };
  CenterSlider.prototype.setX = function (x) { this.track.style.transform = 'translate3d(' + x + 'px,0,0)'; };
  CenterSlider.prototype.mark = function () {
    var pos = this.cur + this.clones;
    this.all.forEach(function (s, k) { s.classList.toggle('is-current', k === pos); });
  };
  CenterSlider.prototype.layout = function () {
    if (!this.root.offsetParent) return;
    this.w = this.width();
    var w = this.w;
    this.all.forEach(function (s) { s.style.width = w + 'px'; });
    this.track.classList.remove('animate');
    this.setX(this.baseX());
    this.mark();
    var self = this;
    clearTimeout(this.alignTimer);
    this.alignTimer = setTimeout(function () { self.alignNav(); }, 560);
  };
  CenterSlider.prototype.go = function (i) {
    var self = this;
    if (this.busy) return;
    this.busy = true;
    setTimeout(function () { self.busy = false; }, 540);
    this.cur = i;
    this.track.classList.add('animate');
    this.setX(this.baseX());
    this.mark();
    clearTimeout(this.snap);
    this.snap = setTimeout(function () {
      var real = ((self.cur % self.n) + self.n) % self.n;
      if (real !== self.cur) {
        self.cur = real;
        self.track.classList.remove('animate');
        self.all.forEach(function (s) { s.style.transition = 'none'; s.querySelectorAll('*').forEach(function (c) { c.style.transition = 'none'; }); });
        self.setX(self.baseX());
        self.mark();
        void self.track.offsetWidth;
        self.all.forEach(function (s) { s.style.transition = ''; s.querySelectorAll('*').forEach(function (c) { c.style.transition = ''; }); });
      }
    }, 520);
  };
  CenterSlider.prototype.stop = function () { clearInterval(this.timer); };
  CenterSlider.prototype.start = function () {
    var self = this;
    this.stop();
    this.timer = setInterval(function () {
      if (self.paused || document.hidden || !self.root.offsetParent) return;
      self.go(self.cur + 1);
    }, 2000 + 500);
  };

  var centerSliders = {};
  $$('[data-slider="projects"]').forEach(function (root) {
    centerSliders[root.closest('.panel').id] = new CenterSlider(root);
  });

  // project tabs
  $$('.tabs .tab a').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var id = 'tab-' + a.getAttribute('data-tab');
      $$('.tabs .tab').forEach(function (t) { t.classList.toggle('active', t === a.parentNode); });
      $$('.tab-panels .panel').forEach(function (p) { p.classList.toggle('active', p.id === id); });
      var s = centerSliders[id];
      if (s) { s.layout(); s.start(); }
    });
  });

  /* ------------------------------------------------------------------
     Why choose us – icon tabs
     ------------------------------------------------------------------ */
  var tabs = $$('.icon-tab');
  var tabWrap = $('.col-tab-l');
  var pointer = document.createElement('span');
  pointer.className = 'why-pointer no-anim';
  tabWrap.appendChild(pointer);
  var panelOf = function (t) { return $('#why-' + t.getAttribute('data-tab')); };

  function placePointer(tab, animate) {
    tabs.forEach(function (t) { var p = panelOf(t); p.style.borderTopLeftRadius = p.style.borderBottomLeftRadius = ''; });
    if (isSmall()) return;
    var panel = panelOf(tab);
    pointer.classList.toggle('no-anim', !animate);
    var h = pointer.offsetHeight, mid = tab.offsetTop + tab.offsetHeight / 2;
    // overlap the panel edge by 1px so arrow + panel read as one shape
    pointer.style.left = (panel.offsetLeft - pointer.offsetWidth + 1) + 'px';
    pointer.style.top = (mid - h / 2) + 'px';
    // square off the panel corner when the arrow sits inside its rounded zone
    var r = 20, top = mid - h / 2 - panel.offsetTop, bottom = panel.offsetTop + panel.offsetHeight - (mid + h / 2);
    panel.style.borderTopLeftRadius = top < r ? '0' : '';
    panel.style.borderBottomLeftRadius = bottom < r ? '0' : '';
  }
  function openAccordion(panel, open) {
    if (open) {
      panel.style.maxHeight = (panel.scrollHeight + 60) + 'px';
    } else {
      panel.style.maxHeight = panel.scrollHeight + 'px';
      void panel.offsetHeight;
      panel.style.maxHeight = '0px';
    }
  }
  function activateTab(tab, animate) {
    tabs.forEach(function (t) {
      var on = t === tab, panel = panelOf(t), was = panel.classList.contains('active');
      if (isSmall() && was !== on) openAccordion(panel, on);
      t.classList.toggle('active', on);
      panel.classList.toggle('active', on);
    });
    placePointer(tab, animate !== false);
  }
  function syncWhyLayout() {
    var active = $('.icon-tab.active') || tabs[0];
    tabs.forEach(function (t) {
      var panel = panelOf(t);
      if (isSmall()) panel.style.maxHeight = t === active ? (panel.scrollHeight + 60) + 'px' : '0px';
      else panel.style.maxHeight = '';
    });
    placePointer(active, false);
  }
  tabs.forEach(function (t) {
    t.addEventListener('click', function () { if (!t.classList.contains('active')) activateTab(t); });
    t.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); activateTab(t); } });
  });
  syncWhyLayout();
  window.addEventListener('resize', syncWhyLayout);
  window.addEventListener('load', syncWhyLayout);

  /* ------------------------------------------------------------------
     Contact form (front-end validation, CF7-like messages)
     ------------------------------------------------------------------ */
  var form = $('.contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      $$('[required]', form).forEach(function (f) {
        var bad = !f.value.trim();
        f.classList.toggle('invalid', bad);
        if (bad) ok = false;
      });
      var email = form.querySelector('[type="email"]');
      if (email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) { email.classList.add('invalid'); ok = false; }
      var res = $('.form-response', form);
      res.classList.toggle('error', !ok);
      res.textContent = ok ? 'Cảm ơn bạn đã gửi tin nhắn. Tin nhắn đã được gửi.'
        : 'Có một hoặc nhiều mục nhập có lỗi. Vui lòng kiểm tra và thử lại.';
      if (ok) form.reset();
    });
    $$('input, textarea', form).forEach(function (f) {
      f.addEventListener('input', function () { f.classList.remove('invalid'); });
    });
  }
})();
