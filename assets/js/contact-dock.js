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
    dock.className = 'contact-dock';
    dock.dataset.contactDock = 'true';
    dock.setAttribute('aria-label', 'Liên hệ nhanh');
    dock.innerHTML = `
      <a class="contact-action contact-zalo" data-contact-action="zalo" data-no-transition
         href="${CONTACT.zalo}"
         aria-label="Mở Zalo FPT Telecom">
        <span class="contact-icon contact-icon-zalo" aria-hidden="true"><span>Zalo</span></span>
        <span class="contact-copy"><strong>Zalo</strong><small>Nhắn tin hỗ trợ</small></span>
      </a>
      <a class="contact-action contact-call" data-contact-action="call" data-no-transition
         href="tel:${CONTACT.phone}" aria-label="Gọi ${CONTACT.phoneLabel}">
        <span class="contact-icon contact-icon-call" aria-hidden="true">
          <svg viewBox="0 0 24 24" focusable="false"><path d="M7.25 3.75 10 7.5 8.4 9.15c1.12 2.08 2.37 3.33 4.45 4.45L14.5 12l3.75 2.75-.85 3.15c-.2.73-.87 1.24-1.63 1.2-6.09-.3-10.57-4.78-10.87-10.87-.04-.76.47-1.43 1.2-1.63l1.15-.31Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </span>
        <span class="contact-copy"><strong>Gọi ngay</strong><small>${CONTACT.phoneLabel}</small></span>
      </a>
      <a class="contact-action contact-register" data-contact-action="register"
         href="${CONTACT.register}" aria-label="Đăng ký tư vấn lắp mạng FPT">
        <span class="contact-icon contact-icon-register" aria-hidden="true">
          <svg viewBox="0 0 24 24" focusable="false"><path d="M8 4.5h8a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2v-11a2 2 0 0 1 2-2Z" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="m8.7 12 2 2.1 4.7-4.8" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </span>
        <span class="contact-copy"><strong>Đăng ký</strong><small>Tư vấn theo địa chỉ</small></span>
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
