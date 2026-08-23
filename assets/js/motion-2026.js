(() => {
  if (window.FPTMotion2026) return;
  const root = document.documentElement;
  const body = document.body;
  if (!body) return;

  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const fine = matchMedia('(hover:hover) and (pointer:fine)');
  const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  const lowPower = Boolean(connection?.saveData) || (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 2);
  const select = (selector, scope = document) => [...scope.querySelectorAll(selector)];
  const unique = (nodes) => [...new Set(nodes.filter(Boolean))];
  const clamp = (v, min, max) => Math.min(max, Math.max(min, v));
  const rafThrottle = (fn) => {
    let raf = 0;
    return (...args) => {
      if (raf) return;
      raf = requestAnimationFrame(() => { raf = 0; fn(...args); });
    };
  };

  root.setAttribute('data-motion-2026', 'booting');
  body.classList.add('motion-2026');

  let progress = document.querySelector('[data-m26-progress]');
  if (!progress) {
    progress = document.createElement('div');
    progress.className = 'm26-progress';
    progress.setAttribute('data-m26-progress', 'true');
    progress.setAttribute('aria-hidden', 'true');
    body.appendChild(progress);
  }

  const headers = unique(select('.hm-header,.topbar,.site-header,body>header')).filter(el => !el.closest('main'));
  headers.forEach(el => el.classList.add('m26-header'));

  const sections = unique(select('main>section,main>.section,main>.hm-shell>section,main>.container>section,.seo-hero,.subpage-hero,.contact-hero,.hm-footer,.footer'));
  sections.forEach((section, i) => {
    section.classList.add('m26-section','m26-scroll-glow');
    section.style.setProperty('--m26-order', String(i));
  });

  const revealSelectors = [
    'main h1','main h2','main h3',
    '.hm-stat','.hm-plan','.hm-solution','.hm-faq details',
    '.m2-feature','.m2-panel','.m2-core-media','.m2-core-copy',
    '.content-card','.owner-link','.package','.use-card','.article','.lead-card','.seo-box',
    '.subpage-hero .wrap>*','.seo-hero>*','.contact-hero>*',
    '.hm-footer-brand','.hm-footer-group','.hm-footer-bottom',
    '.footer-grid>*'
  ];
  const reveal = unique(revealSelectors.flatMap(s => select(s))).filter(node => !node.closest('[aria-hidden="true"]'));
  reveal.forEach((node, i) => {
    node.classList.add('m26-reveal');
    const siblings = node.parentElement ? [...node.parentElement.children] : [];
    const index = Math.max(0, siblings.indexOf(node));
    node.style.setProperty('--m26-delay', `${Math.min(index, 5) * 46}ms`);
    if (node.matches('.m2-core-copy,.subpage-hero .wrap>div:first-child,.seo-hero>div:first-child')) node.dataset.m26Direction = 'left';
    if (node.matches('.m2-core-media,.subpage-hero img,.seo-hero>img')) node.dataset.m26Direction = 'right';
  });

  if (reduce.matches || !('IntersectionObserver' in window)) {
    reveal.forEach(node => node.classList.add('m26-in'));
    sections.forEach(node => node.classList.add('m26-active'));
  } else {
    const revealIO = new IntersectionObserver((entries, io) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('m26-in');
        io.unobserve(entry.target);
      });
    }, { threshold: .06, rootMargin: '0px 0px -7% 0px' });
    reveal.forEach(node => revealIO.observe(node));

    const sectionIO = new IntersectionObserver(entries => {
      entries.forEach(entry => entry.target.classList.toggle('m26-active', entry.isIntersecting));
    }, { threshold: .02, rootMargin: '8% 0px 8% 0px' });
    sections.forEach(node => sectionIO.observe(node));
  }

  const media = unique(select('.hm-photo,.m2-core-media,.seo-hero,.subpage-hero .wrap,.package-media,.use-card,.solution-card,.article figure,main picture'));
  media.forEach(node => node.classList.add('m26-media'));
  const parallax = unique(select('.hm-photo,.m2-core-media,.seo-hero,.subpage-hero .wrap')).filter(node => node.querySelector('img'));
  parallax.forEach(node => node.classList.add('m26-parallax'));

  const navLinks = unique(select('.hm-menu-panel a,.nav-links a,.topbar a,.breadcrumbs a,.hm-footer a,.footer a')).filter(a => {
    const href = a.getAttribute('href') || '';
    return href && !href.startsWith('tel:') && !href.startsWith('mailto:');
  });
  navLinks.forEach(a => a.classList.add('m26-nav-link'));

  const interactive = unique(select('.hm-btn,.btn,button,.hm-dock a,.hm-footer-register,.header-register,.package a,.owner-link,.hm-plan,.hm-solution'));
  interactive.forEach(node => {
    node.classList.add('m26-press');
    node.addEventListener('pointerdown', event => {
      if (reduce.matches || event.button > 0) return;
      const rect = node.getBoundingClientRect();
      const ripple = document.createElement('span');
      ripple.className = 'm26-ripple';
      ripple.setAttribute('aria-hidden','true');
      ripple.style.left = `${clamp(event.clientX - rect.left, 0, rect.width)}px`;
      ripple.style.top = `${clamp(event.clientY - rect.top, 0, rect.height)}px`;
      node.appendChild(ripple);
      ripple.addEventListener('animationend', () => ripple.remove(), { once:true });
    }, { passive:true });
  });

  const tiltTargets = unique(select('.hm-plan,.hm-solution,.m2-feature,.m2-panel,.content-card,.owner-link,.package,.use-card,.lead-card'));
  if (fine.matches && !reduce.matches && !lowPower) {
    tiltTargets.forEach(card => {
      card.classList.add('m26-tilt','m26-spotlight');
      const move = rafThrottle(event => {
        const r = card.getBoundingClientRect();
        const x = clamp((event.clientX - r.left) / Math.max(1, r.width), 0, 1);
        const y = clamp((event.clientY - r.top) / Math.max(1, r.height), 0, 1);
        card.style.setProperty('--m26-ry', `${((x - .5) * 4.2).toFixed(2)}deg`);
        card.style.setProperty('--m26-rx', `${((.5 - y) * 3.6).toFixed(2)}deg`);
        card.style.setProperty('--m26-cx', `${(x * 100).toFixed(1)}%`);
        card.style.setProperty('--m26-cy', `${(y * 100).toFixed(1)}%`);
      });
      card.addEventListener('pointermove', move, { passive:true });
      card.addEventListener('pointerleave', () => {
        card.style.setProperty('--m26-rx','0deg');
        card.style.setProperty('--m26-ry','0deg');
      }, { passive:true });
    });

    const magnetic = unique(select('.hm-btn,.btn,.header-register,.hm-footer-register,.hm-dock .register'));
    magnetic.forEach(node => {
      node.classList.add('m26-magnetic');
      const move = rafThrottle(event => {
        const r = node.getBoundingClientRect();
        const dx = clamp((event.clientX - (r.left + r.width/2)) / Math.max(1, r.width/2), -1, 1) * 5;
        const dy = clamp((event.clientY - (r.top + r.height/2)) / Math.max(1, r.height/2), -1, 1) * 4;
        node.style.setProperty('--m26-mx', `${dx.toFixed(1)}px`);
        node.style.setProperty('--m26-my', `${dy.toFixed(1)}px`);
      });
      node.addEventListener('pointermove', move, { passive:true });
      node.addEventListener('pointerleave', () => {
        node.style.setProperty('--m26-mx','0px');
        node.style.setProperty('--m26-my','0px');
      }, { passive:true });
    });

    const pointerMove = rafThrottle(event => {
      root.style.setProperty('--m26-px', `${(event.clientX / Math.max(1, innerWidth) * 100).toFixed(1)}%`);
      root.style.setProperty('--m26-py', `${(event.clientY / Math.max(1, innerHeight) * 100).toFixed(1)}%`);
    });
    addEventListener('pointermove', pointerMove, { passive:true });
  }

  unique(select('.hm-wifi-badge,.core-neo-float,.m2-core-mini')).forEach((node,i) => {
    node.classList.add('m26-float');
    node.style.setProperty('--m26-float-delay', `${-(i % 4) * 1.1}s`);
  });
  unique(select('.hm-btn-primary,.header-register,.hm-footer-register')).forEach(node => node.classList.add('m26-pulse'));

  const footer = document.querySelector('.hm-footer,.footer');
  footer?.classList.add('m26-footer');

  const updateScroll = rafThrottle(() => {
    if (reduce.matches || document.hidden) return;
    const max = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    const p = clamp(scrollY / max, 0, 1);
    root.style.setProperty('--m26-scroll', p.toFixed(4));
    headers.forEach(h => h.classList.toggle('m26-scrolled', scrollY > 18));

    const vh = Math.max(1, innerHeight);
    parallax.forEach(node => {
      const r = node.getBoundingClientRect();
      if (r.bottom < -120 || r.top > vh + 120) return;
      const center = r.top + r.height/2;
      const normalized = clamp((vh/2 - center) / vh, -.7, .7);
      const strength = innerWidth <= 820 ? 7 : lowPower ? 9 : 16;
      node.style.setProperty('--m26-parallax', `${(normalized * strength).toFixed(1)}px`);
    });
    sections.forEach(section => {
      const r = section.getBoundingClientRect();
      if (r.bottom < -80 || r.top > vh + 80) return;
      const center = r.top + r.height/2;
      const normalized = clamp((vh/2 - center) / vh, -.6, .6);
      section.style.setProperty('--m26-section-y', `${(normalized * (innerWidth <= 820 ? 4 : 9)).toFixed(1)}px`);
    });
    if (footer) {
      const r = footer.getBoundingClientRect();
      const normalized = clamp((vh - r.top) / vh, 0, 1);
      footer.style.setProperty('--m26-footer-y', `${((1-normalized)*18).toFixed(1)}px`);
    }
  });
  addEventListener('scroll', updateScroll, { passive:true });
  addEventListener('resize', updateScroll, { passive:true });
  addEventListener('pageshow', updateScroll, { passive:true });

  reduce.addEventListener?.('change', event => {
    if (event.matches) {
      reveal.forEach(node => node.classList.add('m26-in'));
      root.style.setProperty('--m26-scroll','1');
    } else updateScroll();
  });

  requestAnimationFrame(() => {
    updateScroll();
    root.setAttribute('data-motion-2026', 'ready');
    root.setAttribute('data-motion-coverage', 'full-site-v1');
  });

  window.FPTMotion2026 = Object.freeze({
    version:'2026.1',
    reveal:reveal.length,
    sections:sections.length,
    tilt:tiltTargets.length,
    lowPower,
    reduced:reduce.matches,
    refresh:updateScroll
  });
})();
