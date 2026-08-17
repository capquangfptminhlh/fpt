(() => {
  const cards = [...document.querySelectorAll('[data-premium-plan-card]')];
  if (!cards.length) return;

  const closeOtherDrawers = (exceptCard) => {
    cards.forEach((card) => {
      if (card === exceptCard) return;
      const button = card.querySelector('[data-premium-plan-toggle]');
      const drawer = button ? document.getElementById(button.getAttribute('aria-controls')) : null;
      if (!button || !drawer || drawer.hidden) return;
      drawer.hidden = true;
      button.setAttribute('aria-expanded', 'false');
      button.textContent = 'Xem chi tiết';
    });
  };

  cards.forEach((card) => {
    const button = card.querySelector('[data-premium-plan-toggle]');
    if (button) {
      button.addEventListener('click', () => {
        const drawer = document.getElementById(button.getAttribute('aria-controls'));
        if (!drawer) return;
        const willOpen = drawer.hidden;
        if (willOpen) closeOtherDrawers(card);
        drawer.hidden = !willOpen;
        button.setAttribute('aria-expanded', String(willOpen));
        button.textContent = willOpen ? 'Thu gọn' : 'Xem chi tiết';
      });
    }

    const select = card.querySelector('[data-premium-select-plan]');
    select?.addEventListener('click', () => {
      const plan = select.getAttribute('data-premium-select-plan') || card.getAttribute('data-premium-plan-name') || '';
      const form = document.querySelector('[data-lead-form]');
      if (!form || !plan) return;
      const note = form.elements?.note;
      if (note) {
        const marker = `Gói quan tâm: ${plan}`;
        const current = note.value.trim();
        if (!current.includes(marker)) note.value = current ? `${marker}\n${current}` : marker;
      }
      try {
        sessionStorage.setItem('fptSelectedPlan', plan);
      } catch {}
    });
  });
})();
