(() => {
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const root = document.documentElement;
  const body = document.body;
  if (!body) return;

  const select = (selector, scope = document) => Array.from(scope.querySelectorAll(selector));
  const unique = (nodes) => Array.from(new Set(nodes.filter(Boolean)));
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const supportsIO = 'IntersectionObserver' in window;
  const baseMotion = window.FPTMotionSystem || {};
  const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  const lowPower = Boolean(baseMotion.lowPower) || Boolean(connection?.saveData) || (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 2);

  body.classList.add('full-page-motion-v12');

  // Ambient motion belongs only to structural sections. Never turn nested cards/CTA blocks
  // into independent color layers, because those stacks create visible color contamination.
  const sectionCandidates = unique(select('main > section, main > .m-section, .subpage-hero, .seo-hero, .contact-hero, .footer'));
  const sections = sectionCandidates.filter((node) => {
    if (node.closest('.contact-dock')) return false;
    const parentSection = node.parentElement?.closest('section');
    return !parentSection;
  });

  sections.forEach((section, index) => {
    section.classList.add('motion-section', `motion-tone-${index % 3}`);
    section.style.setProperty('--section-order', String(index));
    if (!section.querySelector(':scope > .motion-section-beam')) {
      const beam = document.createElement('span');
      beam.className = 'motion-section-beam';
      beam.setAttribute('aria-hidden', 'true');
      section.prepend(beam);
    }
  });

  const headings = select('main h1,main h2,main h3,.footer h2,.footer h3').filter((node) => {
    return !node.closest('.contact-dock') && !node.closest('[aria-hidden="true"]');
  });
  headings.forEach((heading, index) => {
    heading.classList.add('motion-heading');
    heading.style.setProperty('--heading-delay', `${Math.min(index % 4, 3) * 50}ms`);
  });

  const mediaSelectors = [
    '.m-hero-media img', '.solution-card img', '.eco-main img', '.eco-stack img', '.seo-hero img',
    '.subpage-hero img', '.use-card img', '.article img', '.content-card img', 'main figure img', 'main picture img'
  ];
  const media = unique(mediaSelectors.flatMap((selector) => select(selector))).filter((node) => {
    const src = (node.getAttribute('src') || '').toLowerCase();
    const classes = String(node.className || '').toLowerCase();
    return !src.includes('logo') && !classes.includes('logo') && !classes.includes('icon');
  });
  media.forEach((node) => node.classList.add('motion-cinematic-media'));

  const navLinks = unique(select('.topbar a,.nav a,.breadcrumbs a,.footer a')).filter((node) => {
    const href = node.getAttribute('href') || '';
    return href && !href.startsWith('tel:') && !href.startsWith('mailto:') && !node.closest('.contact-dock');
  });
  navLinks.forEach((node) => node.classList.add('motion-nav-link'));

  const depthTargets = unique(select('.m-plan,.solution-card,.package,.use-card,.content-card,.article,.lead-card,.contact-callout'));
  depthTargets.forEach((node) => node.classList.add('motion-depth-soft'));

  const footer = document.querySelector('.footer');
  if (footer && !footer.querySelector('.motion-footer-field')) {
    footer.classList.add('motion-footer');
    const field = document.createElement('div');
    field.className = 'motion-footer-field';
    field.setAttribute('aria-hidden', 'true');
    field.innerHTML = '<i></i><i></i><i></i>';
    footer.prepend(field);
  }

  const showEverything = () => {
    headings.forEach((node) => node.classList.add('is-motion-heading-visible'));
    media.forEach((node) => node.classList.add('is-motion-media-visible'));
    sections.forEach((node) => node.classList.add('is-motion-section-active'));
  };

  const activeSections = new Set();
  if (reduceMotion.matches || !supportsIO) {
    showEverything();
    sections.forEach((node) => activeSections.add(node));
  } else {
    const headingObserver = new IntersectionObserver((entries, io) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-motion-heading-visible');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    headings.forEach((node) => headingObserver.observe(node));

    const mediaObserver = new IntersectionObserver((entries, io) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-motion-media-visible');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -5% 0px', threshold: 0.08 });
    media.forEach((node) => mediaObserver.observe(node));

    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        entry.target.classList.toggle('is-motion-section-active', entry.isIntersecting);
        if (entry.isIntersecting) activeSections.add(entry.target);
        else activeSections.delete(entry.target);
      });
    }, { rootMargin: '10% 0px 10% 0px', threshold: 0.02 });
    sections.forEach((node) => sectionObserver.observe(node));
  }

  const rippleTargets = unique(select('.m-btn,.btn,button,.hotline')).filter((node) => !node.closest('.contact-dock'));
  rippleTargets.forEach((node) => {
    node.classList.add('motion-ripple-host');
    node.addEventListener('pointerdown', (event) => {
      if (reduceMotion.matches) return;
      const rect = node.getBoundingClientRect();
      const ripple = document.createElement('span');
      ripple.className = 'motion-ripple';
      ripple.setAttribute('aria-hidden', 'true');
      ripple.style.left = `${clamp(event.clientX - rect.left, 0, rect.width)}px`;
      ripple.style.top = `${clamp(event.clientY - rect.top, 0, rect.height)}px`;
      node.appendChild(ripple);
      ripple.addEventListener('animationend', () => ripple.remove(), { once: true });
    });
  });

  let pointerRaf = 0;
  if (finePointer.matches && !reduceMotion.matches && !lowPower) {
    body.addEventListener('pointermove', (event) => {
      if (pointerRaf) return;
      pointerRaf = requestAnimationFrame(() => {
        pointerRaf = 0;
        root.style.setProperty('--page-pointer-x', `${clamp(event.clientX / Math.max(1, innerWidth) * 100, 0, 100).toFixed(1)}%`);
        root.style.setProperty('--page-pointer-y', `${clamp(event.clientY / Math.max(1, innerHeight) * 100, 0, 100).toFixed(1)}%`);
      });
    }, { passive: true });
  }

  const applySectionMotion = (section, progress, shift) => {
    const mobile = innerWidth <= 760;
    const sectionOpacity = mobile ? .12 + progress * .18 : .16 + progress * .24;
    const blueAlpha = mobile ? .006 + progress * .012 : .008 + progress * .018;
    const warmAlpha = mobile ? .004 + progress * .008 : .006 + progress * .012;
    const lineScale = .62 + progress * .38;
    const lineOpacity = mobile ? .08 + progress * .12 : .12 + progress * .20;
    section.style.setProperty('--section-progress', progress.toFixed(3));
    section.style.setProperty('--section-shift', `${shift.toFixed(1)}px`);
    section.style.setProperty('--section-opacity', sectionOpacity.toFixed(3));
    section.style.setProperty('--section-blue-alpha', blueAlpha.toFixed(3));
    section.style.setProperty('--section-warm-alpha', warmAlpha.toFixed(3));
    section.style.setProperty('--section-line-scale', lineScale.toFixed(3));
    section.style.setProperty('--section-line-opacity', lineOpacity.toFixed(3));
  };

  let scrollTicking = false;
  const updateFullPageScroll = () => {
    scrollTicking = false;
    if (document.hidden || reduceMotion.matches) return;
    const viewport = Math.max(1, innerHeight);
    const targets = activeSections.size ? Array.from(activeSections) : sections;
    targets.forEach((section) => {
      const rect = section.getBoundingClientRect();
      if (rect.bottom < -viewport * .15 || rect.top > viewport * 1.15) return;
      const center = rect.top + rect.height / 2;
      const distance = Math.abs(center - viewport / 2);
      const reach = viewport / 2 + rect.height / 2;
      const progress = 1 - clamp(distance / Math.max(1, reach), 0, 1);
      const normalized = clamp((viewport / 2 - center) / Math.max(viewport, rect.height), -.5, .5);
      const shiftStrength = innerWidth <= 760 ? 6 : lowPower ? 8 : 12;
      applySectionMotion(section, progress, normalized * shiftStrength);
    });
  };

  const scheduleFullPageScroll = () => {
    if (scrollTicking) return;
    scrollTicking = true;
    requestAnimationFrame(updateFullPageScroll);
  };
  addEventListener('scroll', scheduleFullPageScroll, { passive: true });
  addEventListener('resize', scheduleFullPageScroll, { passive: true });
  scheduleFullPageScroll();

  const resetMotion = () => {
    sections.forEach((section) => {
      applySectionMotion(section, 1, 0);
      section.classList.add('is-motion-section-active');
    });
    headings.forEach((node) => node.classList.add('is-motion-heading-visible'));
    media.forEach((node) => node.classList.add('is-motion-media-visible'));
  };

  reduceMotion.addEventListener?.('change', (event) => {
    if (event.matches) resetMotion();
    else scheduleFullPageScroll();
  });
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) scheduleFullPageScroll();
  });
  addEventListener('pageshow', () => {
    if (reduceMotion.matches) resetMotion();
    else scheduleFullPageScroll();
  });

  window.FPTFullPageMotion = Object.freeze({
    version: '12',
    sections: sections.length,
    headings: headings.length,
    media: media.length,
    lowPower,
    refresh: scheduleFullPageScroll
  });
})();
