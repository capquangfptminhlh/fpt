(() => {
  const intentButtons = document.querySelectorAll('[data-intent]');
  const plans = document.querySelectorAll('[data-plan]');
  const recommendation = {
    all: ['giga', 'sky', 'meta'],
    small: ['giga', 'sky'],
    multi: ['sky', 'meta'],
    game: ['sky', 'meta'],
    upload: ['meta', 'sky']
  };

  const setIntent = (intent) => {
    intentButtons.forEach((button) => {
      const active = button.dataset.intent === intent;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });

    const visible = recommendation[intent] || recommendation.all;
    plans.forEach((plan) => {
      const show = visible.includes(plan.dataset.plan);
      plan.hidden = !show;
    });
  };

  intentButtons.forEach((button) => {
    button.addEventListener('click', () => setIntent(button.dataset.intent));
  });

  const availabilityForm = document.querySelector('#availability-form');
  if (availabilityForm) {
    availabilityForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const address = availabilityForm.querySelector('[name="address"]')?.value.trim() || '';
      const need = availabilityForm.querySelector('[name="need"]')?.value || '';
      const params = new URLSearchParams();
      if (address) params.set('address', address);
      if (need) params.set('need', need);
      window.location.href = `/lien-he/${params.toString() ? `?${params}` : ''}`;
    });
  }

  document.querySelectorAll('[data-scroll-plans]').forEach((button) => {
    button.addEventListener('click', (event) => {
      const target = document.querySelector('#goi-cuoc');
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
})();
