(() => {
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const root = document.documentElement;
  const body = document.body;
  if (!body) return;

  const select = (selector, scope = document) => Array.from(scope.querySelectorAll(selector));
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const supportsIO = 'IntersectionObserver' in window;
  const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  const lowPower = Boolean(connection?.saveData) || (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 2);

  const progress = document.createElement('div');
  progress.className = 'motion-progress';
  progress.setAttribute('aria-hidden', 'true');
  progress.innerHTML = '<i></i>';
  body.appendChild(progress);

  const revealTargets = [
    '.m-head', '.availability', '.m-plan', '.solution-card', '.eco-main', '.eco-stack>article',
    '.process article', '.trust-band', '.faq-pro', '.final-cta', '.subpage-hero .wrap>div',
    '.subpage-hero .wrap>img', '.seo-hero .inner', '.content-card', '.package', '.use-card',
    '.article', '.lead-bar', '.faq', '.contact-hero', '.lead-card', '.contact-section', '.contact-callout'
  ];
  const staggerGroups = [
    '.plan-grid', '.solution-grid', '.process', '.trust-points', '.packages', '.use-cases',
    '.article-grid', '.link-grid', '.cluster-index', '.footer-grid'
  ];

  revealTargets.forEach((selector) => {
    select(selector).forEach((node, index) => {
      if (!node.dataset.reveal) node.dataset.reveal = index % 3 === 1 ? 'zoom' : 'up';
    });
  });
  staggerGroups.forEach((selector) => {
    select(selector).forEach((group) => {
      group.classList.add('motion-stagger');
      Array.from(group.children).forEach((child, index) => child.style.setProperty('--stagger-index', String(Math.min(index, 8))));
    });
  });

  const revealNodes = select('[data-reveal], .motion-stagger');
  const revealAll = () => revealNodes.forEach((node) => node.classList.add('is-visible'));
  if (reduceMotion.matches || !supportsIO) {
    revealAll();
  } else {
    body.classList.add('motion-ready');
    const observer = new IntersectionObserver((entries, io) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealNodes.forEach((node) => observer.observe(node));
  }

  const glowSelectors = '.m-plan,.solution-card,.eco-main,.eco-stack>article,.package,.content-card,.lead-card,.contact-callout';
  select(glowSelectors).forEach((node) => node.classList.add('motion-glow'));
  const tiltNodes = select('.m-plan,.solution-card,.eco-main,.eco-stack>article');
  tiltNodes.forEach((node) => node.classList.add('motion-tilt'));
  const magneticNodes = select('.m-btn,.btn,.hotline,.contact-action').filter((node) => !node.closest('.contact-dock') || finePointer.matches);
  magneticNodes.forEach((node) => node.classList.add('motion-magnetic'));

  const hero = document.querySelector('.home-v2 .m-hero');
  const heroMedia = document.querySelector('.home-v2 .m-hero-media');
  if (heroMedia && !heroMedia.querySelector('.motion-signal-field')) {
    const signal = document.createElement('div');
    signal.className = 'motion-signal-field';
    signal.setAttribute('aria-hidden', 'true');
    signal.innerHTML = '<i></i><i></i><i></i><b></b>';
    heroMedia.appendChild(signal);
  }

  let fiberController = null;
  const initFiberField = () => {
    if (!hero || reduceMotion.matches || lowPower || !window.HTMLCanvasElement) return null;
    const canvas = document.createElement('canvas');
    canvas.className = 'motion-fiber-canvas';
    canvas.setAttribute('aria-hidden', 'true');
    hero.prepend(canvas);
    const ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return null;

    let w = 0;
    let h = 0;
    let dpr = 1;
    let raf = 0;
    let active = true;
    let points = [];
    const countForWidth = () => innerWidth < 760 ? 10 : innerWidth < 1100 ? 17 : 25;
    const seedPoints = () => {
      points = Array.from({ length: countForWidth() }, (_, index) => ({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - .5) * .16,
        vy: (Math.random() - .5) * .12,
        r: 1.1 + Math.random() * 1.8,
        warm: index % 4 === 0
      }));
    };
    const resize = () => {
      const rect = hero.getBoundingClientRect();
      w = Math.max(1, rect.width);
      h = Math.max(1, rect.height);
      dpr = Math.min(devicePixelRatio || 1, 1.75);
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      canvas.style.width = `${w}px`;
      canvas.style.height = `${h}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      seedPoints();
    };
    const frame = (time) => {
      raf = 0;
      if (!active || document.hidden || reduceMotion.matches) return;
      ctx.clearRect(0, 0, w, h);
      const maxDistance = innerWidth < 760 ? 105 : 145;
      for (const point of points) {
        point.x += point.vx;
        point.y += point.vy;
        if (point.x < -12) point.x = w + 12;
        if (point.x > w + 12) point.x = -12;
        if (point.y < -12) point.y = h + 12;
        if (point.y > h + 12) point.y = -12;
      }
      for (let a = 0; a < points.length; a += 1) {
        const p = points[a];
        for (let b = a + 1; b < points.length; b += 1) {
          const q = points[b];
          const dx = p.x - q.x;
          const dy = p.y - q.y;
          const dist = Math.hypot(dx, dy);
          if (dist > maxDistance) continue;
          const alpha = (1 - dist / maxDistance) * .15;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(q.x, q.y);
          ctx.strokeStyle = p.warm || q.warm ? `rgba(243,112,33,${alpha.toFixed(3)})` : `rgba(67,153,255,${alpha.toFixed(3)})`;
          ctx.lineWidth = .8;
          ctx.stroke();
        }
      }
      points.forEach((p, index) => {
        const pulse = 1 + Math.sin(time * .0012 + index) * .18;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r * pulse, 0, Math.PI * 2);
        ctx.fillStyle = p.warm ? 'rgba(255,151,82,.48)' : 'rgba(117,184,255,.45)';
        ctx.fill();
      });
      raf = requestAnimationFrame(frame);
    };
    const start = () => {
      active = true;
      if (!raf && !document.hidden && !reduceMotion.matches) raf = requestAnimationFrame(frame);
    };
    const stop = () => {
      active = false;
      if (raf) cancelAnimationFrame(raf);
      raf = 0;
    };
    resize();
    const resizeHandler = () => requestAnimationFrame(resize);
    addEventListener('resize', resizeHandler, { passive: true });
    if (supportsIO) {
      const io = new IntersectionObserver(([entry]) => entry?.isIntersecting ? start() : stop(), { threshold: 0.02 });
      io.observe(hero);
    } else {
      start();
    }
    document.addEventListener('visibilitychange', () => document.hidden ? stop() : start());
    start();
    return { start, stop, canvas };
  };
  fiberController = initFiberField();

  const planCards = select('.home-v2 .m-plan:not([hidden])');
  let planFocusTimer = 0;
  let planIndex = 0;
  let planPaused = false;
  const clearPlanFocus = () => planCards.forEach((node) => node.classList.remove('is-auto-focus'));
  const schedulePlanFocus = (delay = 2200) => {
    clearTimeout(planFocusTimer);
    if (reduceMotion.matches || document.hidden || planPaused || planCards.length < 2) return;
    planFocusTimer = window.setTimeout(() => {
      clearPlanFocus();
      const card = planCards[planIndex % planCards.length];
      card?.classList.add('is-auto-focus');
      planIndex += 1;
      schedulePlanFocus(3200);
    }, delay);
  };
  planCards.forEach((card) => {
    card.addEventListener('pointerenter', () => { planPaused = true; clearPlanFocus(); clearTimeout(planFocusTimer); });
    card.addEventListener('pointerleave', () => { planPaused = false; schedulePlanFocus(1400); });
    card.addEventListener('focusin', () => { planPaused = true; clearPlanFocus(); clearTimeout(planFocusTimer); });
    card.addEventListener('focusout', () => { planPaused = false; schedulePlanFocus(1400); });
  });
  schedulePlanFocus();

  let ticking = false;
  const updateScroll = () => {
    const max = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    const ratio = clamp(scrollY / max, 0, 1);
    root.style.setProperty('--motion-progress', ratio.toFixed(4));
    body.classList.toggle('motion-scrolled', scrollY > 24);
    if (!reduceMotion.matches && hero && scrollY < Math.max(innerHeight * 1.35, 900)) {
      const amount = clamp(scrollY, 0, 650);
      root.style.setProperty('--hero-copy-y', `${(amount * .045).toFixed(1)}px`);
      root.style.setProperty('--hero-media-y', `${(amount * -.075).toFixed(1)}px`);
    }
    ticking = false;
  };
  addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(updateScroll);
  }, { passive: true });
  updateScroll();

  const clearPointerVars = (node) => {
    node.style.removeProperty('--motion-glow-x');
    node.style.removeProperty('--motion-glow-y');
    node.style.removeProperty('--tilt-x');
    node.style.removeProperty('--tilt-y');
  };
  if (finePointer.matches && !reduceMotion.matches) {
    select('.motion-glow').forEach((node) => {
      node.addEventListener('pointermove', (event) => {
        const rect = node.getBoundingClientRect();
        const x = clamp(event.clientX - rect.left, 0, rect.width);
        const y = clamp(event.clientY - rect.top, 0, rect.height);
        node.style.setProperty('--motion-glow-x', `${x}px`);
        node.style.setProperty('--motion-glow-y', `${y}px`);
        if (node.classList.contains('motion-tilt')) {
          const nx = rect.width ? x / rect.width - .5 : 0;
          const ny = rect.height ? y / rect.height - .5 : 0;
          node.style.setProperty('--tilt-y', `${(nx * 5).toFixed(2)}deg`);
          node.style.setProperty('--tilt-x', `${(ny * -4).toFixed(2)}deg`);
        }
      });
      node.addEventListener('pointerleave', () => clearPointerVars(node));
    });
    magneticNodes.forEach((node) => {
      node.addEventListener('pointermove', (event) => {
        const rect = node.getBoundingClientRect();
        const x = (event.clientX - rect.left - rect.width / 2) * .12;
        const y = (event.clientY - rect.top - rect.height / 2) * .12;
        node.classList.add('is-magnetized');
        node.style.setProperty('--magnet-x', `${x.toFixed(1)}px`);
        node.style.setProperty('--magnet-y', `${y.toFixed(1)}px`);
      });
      node.addEventListener('pointerleave', () => {
        node.classList.remove('is-magnetized');
        node.style.setProperty('--magnet-x', '0px');
        node.style.setProperty('--magnet-y', '0px');
      });
    });
    if (heroMedia) {
      heroMedia.addEventListener('pointermove', (event) => {
        const rect = heroMedia.getBoundingClientRect();
        const nx = (event.clientX - rect.left) / rect.width - .5;
        const ny = (event.clientY - rect.top) / rect.height - .5;
        root.style.setProperty('--hero-ry', `${(nx * 4.5).toFixed(2)}deg`);
        root.style.setProperty('--hero-rx', `${(ny * -3.6).toFixed(2)}deg`);
      });
      heroMedia.addEventListener('pointerleave', () => {
        root.style.setProperty('--hero-ry', '0deg');
        root.style.setProperty('--hero-rx', '0deg');
      });
    }
  }

  select('details').forEach((detail) => {
    detail.addEventListener('toggle', () => {
      if (!detail.open || reduceMotion.matches) return;
      detail.animate([{ transform: 'translateY(-2px)', opacity: .94 }, { transform: 'translateY(0)', opacity: 1 }], { duration: 260, easing: 'cubic-bezier(.22,1,.36,1)' });
    });
  });

  reduceMotion.addEventListener?.('change', (event) => {
    if (!event.matches) return;
    body.classList.remove('motion-ready');
    revealAll();
    fiberController?.stop();
    clearTimeout(planFocusTimer);
    clearPlanFocus();
    root.style.setProperty('--hero-copy-y', '0px');
    root.style.setProperty('--hero-media-y', '0px');
    root.style.setProperty('--hero-rx', '0deg');
    root.style.setProperty('--hero-ry', '0deg');
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      clearTimeout(planFocusTimer);
      clearPlanFocus();
    } else {
      schedulePlanFocus(1800);
    }
  });
  addEventListener('pageshow', () => {
    body.classList.remove('motion-scrolled');
    updateScroll();
    schedulePlanFocus(1800);
  });

  window.FPTMotionSystem = Object.freeze({ version: '10', revealAll, lowPower });
})();
