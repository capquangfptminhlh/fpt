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
        <span class="contact-icon" aria-hidden="true">Z</span>
        <span class="contact-copy"><strong>Zalo</strong><small>Nhắn tin hỗ trợ</small></span>
      </a>
      <a class="contact-action contact-call" data-contact-action="call" data-no-transition
         href="tel:${CONTACT.phone}" aria-label="Gọi ${CONTACT.phoneLabel}">
        <span class="contact-icon" aria-hidden="true">☎</span>
        <span class="contact-copy"><strong>Gọi ngay</strong><small>${CONTACT.phoneLabel}</small></span>
      </a>
      <a class="contact-action contact-register" data-contact-action="register"
         href="${CONTACT.register}" aria-label="Đăng ký tư vấn lắp mạng FPT">
        <span class="contact-icon" aria-hidden="true">✓</span>
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
