(() => {
  const root = document.body;
  if (!root?.hasAttribute('data-package-count')) return;

  // Dedicated 2026 segmented-filter visual authority. Reuse this script's cache-bust token.
  if (!document.querySelector('[data-package-tabs-2026]')) {
    const style = document.createElement('link');
    style.rel = 'stylesheet';
    const scriptSrc = document.currentScript?.src || '';
    const version = new URL(scriptSrc || location.href, location.href).searchParams.get('v') || '20260824-1';
    style.href = `/fpt/assets/css/package-tabs-2026.css?v=${encodeURIComponent(version)}`;
    style.setAttribute('data-package-tabs-2026', 'true');
    document.head.appendChild(style);
  }

  // Keep the interface concise while preserving category meaning and counts.
  const shortLabels = {
    all: 'Tất cả',
    internet: 'Internet',
    game: 'Gaming',
    combo: 'Combo',
    wifi7: 'Wi‑Fi 7',
    camera: 'Camera',
    business: 'Doanh nghiệp'
  };
  const fullLabels = {
    all: 'Tất cả gói cước',
    internet: 'Internet gia đình',
    game: 'Game thủ',
    combo: 'Combo Internet và FPT Play',
    wifi7: 'Wi‑Fi 7 SpeedX',
    camera: 'Internet và Camera',
    business: 'Doanh nghiệp'
  };

  const input = document.querySelector('#pkg-search');
  const count = document.querySelector('#pkg-result-count');
  const cards = [...document.querySelectorAll('.pkg-card')];
  const sections = [...document.querySelectorAll('[data-pkg-section]')];
  const buttons = [...document.querySelectorAll('[data-pkg-filter]')];
  let filter = 'all';

  buttons.forEach((btn) => {
    const key = btn.dataset.pkgFilter;
    const badge = btn.querySelector('b');
    const amount = badge?.textContent?.trim() || '';
    btn.innerHTML = `${shortLabels[key] || key}${amount ? ` <b>${amount}</b>` : ''}`;
    btn.setAttribute('aria-label', `${fullLabels[key] || shortLabels[key] || key}${amount ? `, ${amount} gói` : ''}`);
    btn.setAttribute('aria-pressed', String(btn.classList.contains('active')));
  });

  // Remove the public-source wording from the rendered catalog while retaining update-date transparency.
  const heroChip = document.querySelector('.pkg-hero .hm-chip');
  if (heroChip && /fpt\.vn/i.test(heroChip.textContent || '')) heroChip.textContent = 'Cập nhật 23/08/2026';
  const heroNote = document.querySelector('.pkg-hero-panel p');
  if (heroNote) heroNote.textContent = 'Giá trên trang là mức tham khảo tại thời điểm cập nhật. Chính sách thực tế phụ thuộc khu vực, hạ tầng và chương trình khuyến mãi.';

  const norm = (s) => (s || '').toLocaleLowerCase('vi').normalize('NFD').replace(/\p{Diacritic}/gu, '');
  const apply = () => {
    const q = norm(input?.value.trim());
    let visible = 0;
    cards.forEach((card) => {
      const okCat = filter === 'all' || card.dataset.pkgCategory === filter;
      const okText = !q || norm(card.textContent).includes(q);
      const show = okCat && okText;
      card.hidden = !show;
      if (show) visible++;
    });
    sections.forEach((section) => {
      section.hidden = ![...section.querySelectorAll('.pkg-card')].some((card) => !card.hidden);
    });
    if (count) count.textContent = `${visible} gói`;
  };

  buttons.forEach((btn) => btn.addEventListener('click', () => {
    filter = btn.dataset.pkgFilter;
    buttons.forEach((button) => {
      const active = button === btn;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    btn.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'nearest', inline: 'center' });
    apply();
  }));

  input?.addEventListener('input', apply);
  apply();
  document.documentElement.setAttribute('data-package-tabs-2026', 'ready');
})();
