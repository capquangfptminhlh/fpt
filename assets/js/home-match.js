(() => {
  const body = document.body;
  if (!body?.classList.contains('fpt-match')) return;

  // Tech typography: Space Grotesk for display + Manrope for UI/body.
  const verifyTechFonts = () => {
    if (!('fonts' in document)) {
      document.documentElement.setAttribute('data-tech-fonts-ready', 'unsupported');
      return;
    }
    Promise.all([
      document.fonts.load('700 32px "Space Grotesk"'),
      document.fonts.load('400 16px "Manrope"')
    ]).then(() => {
      const fontsReady = document.fonts.check('700 32px "Space Grotesk"') && document.fonts.check('400 16px "Manrope"');
      document.documentElement.setAttribute('data-tech-fonts-ready', String(fontsReady));
    }).catch(() => document.documentElement.setAttribute('data-tech-fonts-ready', 'false'));
  };

  let techTypeStyle = document.querySelector('[data-tech-type-style]');
  if (!techTypeStyle) {
    techTypeStyle = document.createElement('link');
    techTypeStyle.rel = 'stylesheet';
    techTypeStyle.href = '/fpt/assets/css/tech-type.css?v=20260823-1';
    techTypeStyle.setAttribute('data-tech-type-style', 'true');
    techTypeStyle.addEventListener('load', verifyTechFonts, { once: true });
    techTypeStyle.addEventListener('error', () => document.documentElement.setAttribute('data-tech-fonts-ready', 'false'), { once: true });
    document.head.appendChild(techTypeStyle);
  } else if (techTypeStyle.sheet) {
    verifyTechFonts();
  } else {
    techTypeStyle.addEventListener('load', verifyTechFonts, { once: true });
  }
  document.documentElement.setAttribute('data-tech-type', 'space-grotesk-manrope-v1');

  // Remove public-facing fpt.vn references while keeping the identity disclaimer.
  const scrubFptVnReferences = () => {
    document.querySelectorAll('a[href*="fpt.vn"]').forEach((link) => {
      const text = (link.textContent || '').trim();
      if (/fpt\.vn/i.test(text)) link.remove();
    });
    const meta = document.querySelector('meta[name="description"]');
    if (meta?.content) {
      meta.content = meta.content
        .replace(/\s*(?:đối chiếu|cập nhật)\s+từ\s+FPT\.vn[:,]?\s*/gi, ' ')
        .replace(/FPT\.vn/gi, '')
        .replace(/\s{2,}/g, ' ')
        .trim();
    }
    const walker = document.createTreeWalker(body, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach((node) => {
      if (!/fpt\.vn/i.test(node.nodeValue || '')) return;
      node.nodeValue = node.nodeValue
        .replace(/Đối chiếu\s+FPT\.vn\s*·?\s*/gi, 'Cập nhật ')
        .replace(/(?:được\s+)?FPT\.vn\s+hiển thị/gi, 'được cập nhật')
        .replace(/(?:đối chiếu|cập nhật)\s+từ\s+FPT\.vn/gi, 'đã cập nhật')
        .replace(/FPT\.vn/gi, '')
        .replace(/\s{2,}/g, ' ');
    });
    document.documentElement.setAttribute('data-fptvn-public', 'removed');
  };
  scrubFptVnReferences();

  // Advertising / identity transparency. This is intentionally prominent on every Match page.
  if (!document.getElementById('hm-sales-disclosure-style')) {
    const disclosureStyle = document.createElement('style');
    disclosureStyle.id = 'hm-sales-disclosure-style';
    disclosureStyle.textContent = `
      .hm-sales-disclosure{position:relative;z-index:40;background:#fff7ed;border-top:1px solid #fed7aa;border-bottom:1px solid #fed7aa;color:#7c2d12;font:650 12px/1.55 Manrope,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
      .hm-sales-disclosure-inner{max-width:1180px;margin:0 auto;padding:9px 22px;display:flex;align-items:center;justify-content:center;gap:7px;text-align:center}
      .hm-sales-disclosure strong{font-weight:850;color:#9a3412}
      .hm-footer-disclosure{margin-top:12px;padding-top:12px;border-top:1px solid rgba(15,35,63,.10);font-size:12px;line-height:1.65;color:#667085}
      .hm-footer-disclosure strong{color:#344054}
      @media(max-width:820px){.hm-sales-disclosure-inner{padding:8px 14px;font-size:11px;line-height:1.5}.hm-sales-disclosure{position:relative}.hm-footer-disclosure{font-size:11px}}
    `;
    document.head.appendChild(disclosureStyle);
  }

  if (!document.querySelector('[data-sales-disclosure]')) {
    const disclosure = document.createElement('aside');
    disclosure.className = 'hm-sales-disclosure';
    disclosure.setAttribute('data-sales-disclosure', 'true');
    disclosure.setAttribute('aria-label', 'Thông tin minh bạch về website');
    disclosure.innerHTML = '<div class="hm-sales-disclosure-inner"><span><strong>Trang tư vấn của nhân viên kinh doanh FPT Telecom.</strong> Đây không phải website chính thức của Công ty Cổ phần Viễn thông FPT.</span></div>';
    const main = document.querySelector('main');
    const menu = document.querySelector('[data-hm-menu-panel]');
    if (main) main.before(disclosure);
    else if (menu) menu.after(disclosure);
    else body.prepend(disclosure);
    document.documentElement.setAttribute('data-sales-disclosure', 'ready');
  }

  // Footer v2: compact, light, shared by homepage + primary/package pages.
  if (!document.querySelector('[data-hm-footer-style]')) {
    const footerStyle = document.createElement('link');
    footerStyle.rel = 'stylesheet';
    footerStyle.href = '/fpt/assets/css/site-footer-v2.css?v=20260823-1';
    footerStyle.setAttribute('data-hm-footer-style', 'true');
    document.head.appendChild(footerStyle);
  }

  if (!document.querySelector('[data-hm-footer]')) {
    const footer = document.createElement('footer');
    footer.className = 'hm-footer';
    footer.setAttribute('data-hm-footer', 'true');
    footer.innerHTML = `
      <div class="hm-shell">
        <div class="hm-footer-top">
          <div class="hm-footer-brand">
            <a href="/fpt/" aria-label="Trang tư vấn Internet FPT"><img src="/fpt/assets/images/logo-fpt.svg" width="154" height="41" alt="FPT Telecom"/></a>
            <p>Internet, WiFi, Camera và FPT Play cho gia đình. Giá, thiết bị và ưu đãi được xác nhận theo khu vực trước khi đăng ký.</p>
          </div>
          <div class="hm-footer-links">
            <section class="hm-footer-group" aria-labelledby="hm-footer-services">
              <h2 id="hm-footer-services">Dịch vụ</h2>
              <a href="/fpt/internet-fpt/">Internet FPT</a>
              <a href="/fpt/goi-cuoc-fpt/">Gói cước</a>
              <a href="/fpt/wifi-7/">WiFi 7 & Mesh</a>
              <a href="/fpt/camera-fpt/">Camera FPT</a>
            </section>
            <section class="hm-footer-group" aria-labelledby="hm-footer-support">
              <h2 id="hm-footer-support">Hỗ trợ</h2>
              <a href="/fpt/khu-vuc/">Kiểm tra khu vực</a>
              <a href="/fpt/ho-tro/">Trung tâm hỗ trợ</a>
              <a href="/fpt/fpt-play/">FPT Play</a>
              <a href="/fpt/combo-fpt/">Combo FPT</a>
            </section>
            <section class="hm-footer-group" aria-labelledby="hm-footer-contact">
              <h2 id="hm-footer-contact">Liên hệ</h2>
              <a class="hm-footer-phone" href="tel:19006600"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M7.1 3.7 10 7.4 8.4 9c1.12 2.08 2.38 3.34 4.46 4.46l1.62-1.62 3.78 2.77-.9 3.08c-.22.75-.9 1.25-1.69 1.2C9.69 18.54 5.34 14.2 4.99 8.28c-.05-.79.45-1.47 1.2-1.69l.91-2.89Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>1900 6600</a>
              <a href="https://zalo.me/fpttelecom" data-no-transition>Chat Zalo</a>
              <a class="hm-footer-register" href="/fpt/lien-he/">Đăng ký tư vấn</a>
            </section>
          </div>
        </div>
        <div class="hm-footer-bottom">
          <p>© 2026 Trang tư vấn Internet FPT · Kênh tư vấn nhân viên kinh doanh.</p>
          <p><a href="/fpt/chinh-sach-cap-nhat/">Chính sách cập nhật</a></p>
        </div>
        <div class="hm-footer-disclosure"><strong>Tuyên bố minh bạch:</strong> Website này là trang tư vấn bán hàng do nhân viên kinh doanh FPT Telecom vận hành và <strong>không phải website chính thức của Công ty Cổ phần Viễn thông FPT</strong>. Nội dung về giá, ưu đãi, thiết bị và phạm vi cung cấp cần được xác nhận tại thời điểm đăng ký.</div>
      </div>`;

    const dock = document.querySelector('.hm-dock');
    if (dock) dock.before(footer);
    else document.body.appendChild(footer);
  }

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
