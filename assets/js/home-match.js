(() => {
  const body = document.body;
  if (!body?.classList.contains('fpt-match')) return;

  const menuButton = document.querySelector('[data-hm-menu-button]');
  const menuPanel = document.querySelector('[data-hm-menu-panel]');
  const closeMenu = () => {
    menuPanel?.classList.remove('open');
    menuButton?.setAttribute('aria-expanded', 'false');
  };

  menuButton?.addEventListener('click', (event) => {
    event.stopPropagation();
    const open = !menuPanel?.classList.contains('open');
    menuPanel?.classList.toggle('open', open);
    menuButton.setAttribute('aria-expanded', String(open));
  });

  document.addEventListener('click', (event) => {
    if (!menuPanel?.contains(event.target) && !menuButton?.contains(event.target)) closeMenu();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeMenu();
  });

  menuPanel?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));

  const reveal = [...document.querySelectorAll('.hm-reveal')];
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) {
    reveal.forEach((node) => node.classList.add('is-in'));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -5% 0px' });
    reveal.forEach((node) => io.observe(node));
  }

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const target = document.querySelector(link.getAttribute('href'));
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
})();
