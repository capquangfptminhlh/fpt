(() => {
  const SITE_BASE = location.hostname === 'capquangfptminhlh.github.io' ? '/fpt' : '';
  const sitePath = (path = '/') => `${SITE_BASE}${path.startsWith('/') ? path : `/${path}`}`;
  const CONTACT = Object.freeze({
    phone: '19006600',
    phoneLabel: '1900 6600',
    zalo: 'https://zalo.me/fpttelecom',
    register: sitePath('/lien-he/')
  });

  const boot = () => {
    document.querySelectorAll('.mobile-bottom-cta').forEach((node) => node.remove());
    document.body.classList.remove('has-mobile-cta');
    if (document.querySelector('[data-contact-dock]')) return;

    const dock = document.createElement('nav');
    dock.className = 'contact-dock contact-dock-v10';
    dock.dataset.contactDock = 'true';
    dock.setAttribute('aria-label', 'Liên hệ nhanh');
    dock.innerHTML = `
      <span class="contact-rail-glow" aria-hidden="true"></span>
      <a class="contact-action contact-zalo" data-contact-action="zalo" data-no-transition
         href="${CONTACT.zalo}" aria-label="Mở Zalo FPT Telecom">
        <span class="contact-visual" aria-hidden="true">
          <span class="contact-orbit"></span>
          <span class="contact-icon contact-icon-zalo"><span>Zalo</span></span>
        </span>
        <span class="contact-copy"><strong>Zalo</strong><small>Chat hỗ trợ</small></span>
      </a>
      <a class="contact-action contact-call" data-contact-action="call" data-no-transition
         href="tel:${CONTACT.phone}" aria-label="Gọi ${CONTACT.phoneLabel}">
        <span class="contact-visual" aria-hidden="true">
          <span class="contact-orbit"></span>
          <span class="contact-icon contact-icon-call">
            <svg viewBox="0 0 24 24" focusable="false"><path d="M7.1 3.8 10 7.5 8.4 9.15c1.12 2.08 2.37 3.33 4.45 4.45L14.5 12l3.75 2.75-.88 3.06c-.21.75-.9 1.25-1.68 1.2C9.7 18.65 5.35 14.3 4.99 8.31c-.05-.78.45-1.47 1.2-1.68L7.1 3.8Z" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </span>
        </span>
        <span class="contact-copy"><strong>Gọi ngay</strong><small>${CONTACT.phoneLabel}</small></span>
      </a>
      <a class="contact-action contact-register" data-contact-action="register"
         href="${CONTACT.register}" aria-label="Đăng ký tư vấn lắp mạng FPT">
        <span class="contact-visual" aria-hidden="true">
          <span class="contact-orbit"></span>
          <span class="contact-icon contact-icon-register">
            <svg viewBox="0 0 24 24" focusable="false"><path d="M8 4.5h8a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2v-11a2 2 0 0 1 2-2Z" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="m8.7 12 2 2.1 4.7-4.8" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </span>
        </span>
        <span class="contact-copy"><strong>Đăng ký</strong><small>Tư vấn nhanh</small></span>
      </a>
    `;

    dock.addEventListener('click', (event) => {
      const action = event.target.closest('[data-contact-action]')?.dataset.contactAction;
      if (!action) return;
      window.dataLayer?.push?.({ event: 'contact_action', contact_action: action, page_path: location.pathname });
    });

    document.body.appendChild(dock);
    document.body.classList.add('has-contact-dock');
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot, { once: true });
  } else {
    boot();
  }
})();
