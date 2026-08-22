(() => {
  const body = document.body;
  if (!body.classList.contains('fpt-neo')) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const header = document.querySelector('.topbar');
  const progress = document.querySelector('.neo-progress');
  const syncScroll = () => {
    header?.classList.toggle('is-scrolled', scrollY > 12);
    if (progress) {
      const max = document.documentElement.scrollHeight - innerHeight;
      progress.style.width = `${max > 0 ? Math.min(100, scrollY / max * 100) : 0}%`;
    }
  };
  syncScroll();
  addEventListener('scroll', syncScroll, { passive: true });

  document.querySelectorAll('.neo-btn').forEach((button) => {
    button.addEventListener('pointerdown', (event) => {
      if (reduced) return;
      const rect = button.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const ripple = document.createElement('span');
      ripple.className = 'neo-ripple';
      Object.assign(ripple.style, {
        width: `${size}px`, height: `${size}px`,
        left: `${event.clientX - rect.left - size / 2}px`,
        top: `${event.clientY - rect.top - size / 2}px`
      });
      button.appendChild(ripple);
      ripple.addEventListener('animationend', () => ripple.remove(), { once: true });
    });
  });

  const reveal = document.querySelectorAll('.neo-reveal');
  if (!reduced && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: .12, rootMargin: '0px 0px -45px' });
    reveal.forEach((node) => io.observe(node));
  } else reveal.forEach((node) => node.classList.add('is-visible'));

  const visual = document.querySelector('.neo-visual');
  const photo = visual?.querySelector('.neo-photo');
  if (!reduced && visual && photo && matchMedia('(pointer:fine)').matches) {
    visual.addEventListener('pointermove', (event) => {
      const r = visual.getBoundingClientRect();
      const x = (event.clientX - r.left) / r.width - .5;
      const y = (event.clientY - r.top) / r.height - .5;
      photo.style.transform = `perspective(1300px) rotateY(${(-4 + x * 4).toFixed(2)}deg) rotateX(${(1 - y * 3).toFixed(2)}deg) translate3d(${x * 5}px,${y * 4}px,0)`;
    });
    visual.addEventListener('pointerleave', () => {
      photo.style.transform = 'perspective(1300px) rotateY(-4deg) rotateX(1deg)';
    });
  }

  document.querySelectorAll('[data-scroll]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const target = document.querySelector(link.dataset.scroll || '');
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' });
    });
  });
})();