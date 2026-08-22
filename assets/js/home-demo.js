(() => {
  const root = document.body;
  if (!root.classList.contains('home-demo')) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const header = document.querySelector('.topbar');
  const mobileToggle = document.querySelector('.mobile-toggle');
  const nav = document.querySelector('.nav-links');

  const syncHeader = () => header?.classList.toggle('is-scrolled', window.scrollY > 10);
  syncHeader();
  window.addEventListener('scroll', syncHeader, { passive: true });

  if (mobileToggle && nav) {
    mobileToggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      mobileToggle.setAttribute('aria-expanded', String(open));
      mobileToggle.setAttribute('aria-label', open ? 'Đóng menu' : 'Mở menu');
      mobileToggle.textContent = open ? '×' : '☰';
    });
    nav.addEventListener('click', (event) => {
      if (!event.target.closest('a')) return;
      nav.classList.remove('open');
      mobileToggle.setAttribute('aria-expanded', 'false');
      mobileToggle.textContent = '☰';
    });
  }

  document.querySelectorAll('.fpt-btn, .header-register').forEach((button) => {
    button.addEventListener('pointerdown', (event) => {
      if (reducedMotion) return;
      const rect = button.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const ripple = document.createElement('span');
      ripple.className = 'fpt-ripple';
      ripple.style.width = `${size}px`;
      ripple.style.height = `${size}px`;
      ripple.style.left = `${event.clientX - rect.left - size / 2}px`;
      ripple.style.top = `${event.clientY - rect.top - size / 2}px`;
      button.appendChild(ripple);
      ripple.addEventListener('animationend', () => ripple.remove(), { once: true });
    });
  });

  const revealNodes = document.querySelectorAll('.reveal');
  if (!reducedMotion && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries, io) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px' });
    revealNodes.forEach((node) => observer.observe(node));
  } else {
    revealNodes.forEach((node) => node.classList.add('is-visible'));
  }

  const heroMedia = document.querySelector('.fpt-hero-media');
  const heroImage = heroMedia?.querySelector('img');
  if (!reducedMotion && heroMedia && heroImage && window.matchMedia('(pointer:fine)').matches) {
    heroMedia.addEventListener('pointermove', (event) => {
      const rect = heroMedia.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - .5;
      const y = (event.clientY - rect.top) / rect.height - .5;
      heroImage.style.transform = `scale(1.025) translate(${x * -6}px, ${y * -5}px)`;
    });
    heroMedia.addEventListener('pointerleave', () => {
      heroImage.style.transform = 'scale(1.015) translate(0,0)';
    });
  }

  document.querySelectorAll('[data-scroll-target]').forEach((trigger) => {
    trigger.addEventListener('click', (event) => {
      const selector = trigger.dataset.scrollTarget;
      const target = selector ? document.querySelector(selector) : null;
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' });
    });
  });
})();
