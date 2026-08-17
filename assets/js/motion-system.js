(() => {
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const root = document.documentElement;
  const body = document.body;
  if (!body) return;

  const select = (selector, scope = document) => Array.from(scope.querySelectorAll(selector));
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const supportsIO = 'IntersectionObserver' in window;

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

  const tiltSelectors = '.m-plan,.solution-card,.eco-main,.eco-stack>article';
  const tiltNodes = select(tiltSelectors);
  tiltNodes.forEach((node) => node.classList.add('motion-tilt'));

  const magneticNodes = select('.m-btn,.btn,.hotline,.contact-action').filter((node) => !node.closest('.contact-dock') || finePointer.matches);
  magneticNodes.forEach((node) => node.classList.add('motion-magnetic'));

  let ticking = false;
  const updateScroll = () => {
    const max = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    const ratio = clamp(scrollY / max, 0, 1);
    root.style.setProperty('--motion-progress', ratio.toFixed(4));
    body.classList.toggle('motion-scrolled', scrollY > 24);

    if (!reduceMotion.matches) {
      const hero = document.querySelector('.home-v2 .m-hero');
      if (hero && scrollY < Math.max(innerHeight * 1.35, 900)) {
        const amount = clamp(scrollY, 0, 650);
        root.style.setProperty('--hero-copy-y', `${(amount * .045).toFixed(1)}px`);
        root.style.setProperty('--hero-media-y', `${(amount * -.075).toFixed(1)}px`);
      }
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
          node.style.setProperty('--tilt-y', `${(nx * 5.5).toFixed(2)}deg`);
          node.style.setProperty('--tilt-x', `${(ny * -4.5).toFixed(2)}deg`);
        }
      });
      node.addEventListener('pointerleave', () => clearPointerVars(node));
    });

    magneticNodes.forEach((node) => {
      node.addEventListener('pointermove', (event) => {
        const rect = node.getBoundingClientRect();
        const x = (event.clientX - rect.left - rect.width / 2) * .13;
        const y = (event.clientY - rect.top - rect.height / 2) * .13;
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

    const heroMedia = document.querySelector('.home-v2 .m-hero-media');
    if (heroMedia) {
      heroMedia.addEventListener('pointermove', (event) => {
        const rect = heroMedia.getBoundingClientRect();
        const nx = (event.clientX - rect.left) / rect.width - .5;
        const ny = (event.clientY - rect.top) / rect.height - .5;
        root.style.setProperty('--hero-ry', `${(nx * 5).toFixed(2)}deg`);
        root.style.setProperty('--hero-rx', `${(ny * -4).toFixed(2)}deg`);
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
      detail.animate([
        { transform: 'translateY(-2px)', opacity: .94 },
        { transform: 'translateY(0)', opacity: 1 }
      ], { duration: 260, easing: 'cubic-bezier(.22,1,.36,1)' });
    });
  });

  reduceMotion.addEventListener?.('change', (event) => {
    if (!event.matches) return;
    body.classList.remove('motion-ready');
    revealAll();
    root.style.setProperty('--hero-copy-y', '0px');
    root.style.setProperty('--hero-media-y', '0px');
    root.style.setProperty('--hero-rx', '0deg');
    root.style.setProperty('--hero-ry', '0deg');
  });

  addEventListener('pageshow', () => {
    body.classList.remove('motion-scrolled');
    updateScroll();
  });

  window.FPTMotionSystem = Object.freeze({ version: '8', revealAll });
})();
