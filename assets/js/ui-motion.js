(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const body = document.body;
  if (!body) return;

  const reveal = Array.from(document.querySelectorAll(
    '.m-plan,.package,.solution-card,.use-card,.content-card,.contact-step,.contact-info,.contact-callout,.lead-card,.article,.promo'
  ));
  const media = Array.from(document.querySelectorAll(
    '.m-hero-media img,.subpage-hero img,.seo-hero>img,.solution-card img,.use-card img,.package-media img,.m-plan-media img'
  ));

  reveal.forEach((node) => node.classList.add('ui-reveal'));
  media.forEach((node) => node.classList.add('ui-media'));

  const showAll = () => {
    reveal.forEach((node) => node.classList.add('is-in'));
    media.forEach((node) => node.classList.add('is-in'));
  };

  body.classList.add('ui-motion-ready');

  if (reduce.matches || !('IntersectionObserver' in window)) {
    showAll();
  } else {
    const observer = new IntersectionObserver((entries, io) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.02 });
    [...reveal, ...media].forEach((node) => observer.observe(node));
  }

  let ticking = false;
  const syncHeader = () => {
    ticking = false;
    body.classList.toggle('ui-scrolled', scrollY > 10);
  };
  addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(syncHeader);
  }, { passive: true });
  syncHeader();

  reduce.addEventListener?.('change', (event) => {
    if (event.matches) showAll();
  });
})();
