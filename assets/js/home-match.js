(() => {
  const body = document.body;
  if (!body?.classList.contains('fpt-match')) return;

  // Dock v3: three independent floating actions, no bulky white tray.
  if (!document.getElementById('hm-dock-v3-style')) {
    const style = document.createElement('style');
    style.id = 'hm-dock-v3-style';
    style.textContent = `
      .fpt-match-v2 .hm-dock{position:fixed!important;z-index:1100!important;left:50%!important;right:auto!important;bottom:18px!important;transform:translateX(-50%)!important;width:auto!important;min-height:0!important;height:auto!important;padding:0!important;border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important;display:flex!important;align-items:center!important;gap:10px!important;grid-template-columns:none!important}
      .fpt-match-v2 .hm-dock a{display:flex!important;align-items:center!important;justify-content:center!important;gap:8px!important;height:50px!important;min-width:0!important;padding:0 16px!important;border:1px solid #e5e9ef!important;border-radius:999px!important;background:rgba(255,255,255,.97)!important;color:#10233f!important;box-shadow:0 10px 28px rgba(17,40,72,.13)!important;font-size:12px!important;font-weight:760!important;backdrop-filter:blur(14px)!important;-webkit-backdrop-filter:blur(14px)!important;transition:transform .18s ease,box-shadow .18s ease!important}
      .fpt-match-v2 .hm-dock a:hover{transform:translateY(-2px)!important;box-shadow:0 14px 34px rgba(17,40,72,.17)!important}
      .fpt-match-v2 .hm-dock svg{width:23px!important;height:23px!important;flex:0 0 23px!important}
      .fpt-match-v2 .hm-dock .zalo{color:#2563eb!important}
      .fpt-match-v2 .hm-dock .call{color:#168a4b!important}
      .fpt-match-v2 .hm-dock .register{min-width:138px!important;padding:0 22px!important;border-color:#ff6900!important;background:#ff6900!important;color:#fff!important;box-shadow:0 12px 28px rgba(255,105,0,.23)!important;font-size:13px!important}
      @media(max-width:820px){
        .fpt-match-v2 .hm-dock{bottom:10px!important;gap:8px!important}
        .fpt-match-v2 .hm-dock a{width:48px!important;height:48px!important;padding:0!important;border-radius:50%!important}
        .fpt-match-v2 .hm-dock .zalo span,.fpt-match-v2 .hm-dock .call span{display:none!important}
        .fpt-match-v2 .hm-dock .register{width:auto!important;min-width:126px!important;padding:0 20px!important;border-radius:999px!important}
      }
      @media(max-width:390px){.fpt-match-v2 .hm-dock .register{min-width:118px!important;padding:0 16px!important}}
    `;
    document.head.appendChild(style);
  }

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
