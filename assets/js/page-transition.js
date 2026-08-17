(() => {
  const STORAGE_KEY = 'fptPageTransition';
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let navigating = false;

  const overlay = document.createElement('div');
  overlay.className = 'page-transition';
  overlay.setAttribute('aria-hidden', 'true');
  overlay.innerHTML = `
    <div class="page-transition__stage" role="status" aria-live="polite" aria-label="Đang chuyển trang">
      <div class="page-transition__glow" aria-hidden="true"></div>
      <div class="page-transition__waves" aria-hidden="true"><i></i><i></i><i></i></div>
      <div class="page-transition__modem-wrap" aria-hidden="true">
        <div class="page-transition__modem"><div class="page-transition__leds"><span></span><span></span><span></span></div></div>
      </div>
      <div class="page-transition__track" aria-hidden="true"><span></span></div>
      <p class="page-transition__text">Đang kết nối tới trang mới…</p>
    </div>
  `;
  document.body.appendChild(overlay);

  const show = (arrival = false) => {
    overlay.classList.toggle('is-arrival', arrival);
    overlay.classList.add('is-active');
    overlay.setAttribute('aria-hidden', 'false');
    document.documentElement.classList.add('page-transitioning');
  };

  const hide = () => {
    overlay.classList.remove('is-active', 'is-arrival');
    overlay.setAttribute('aria-hidden', 'true');
    document.documentElement.classList.remove('page-transitioning');
    navigating = false;
  };

  const isSameSiteNavigation = (anchor, event) => {
    if (!anchor || !anchor.href) return false;
    if (anchor.target && anchor.target !== '_self') return false;
    if (anchor.hasAttribute('download')) return false;
    if (event.defaultPrevented || event.button !== 0) return false;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return false;

    const raw = anchor.getAttribute('href') || '';
    if (!raw || raw.startsWith('#') || /^(?:mailto:|tel:|javascript:)/i.test(raw)) return false;

    let next;
    try { next = new URL(anchor.href, location.href); } catch { return false; }
    if (next.origin !== location.origin) return false;

    const currentNoHash = `${location.origin}${location.pathname}${location.search}`;
    const nextNoHash = `${next.origin}${next.pathname}${next.search}`;
    if (currentNoHash === nextNoHash && next.hash) return false;

    if (location.hostname === 'capquangfptminhlh.github.io' && !next.pathname.startsWith('/fpt/')) return false;
    return true;
  };

  const go = (url) => {
    if (navigating) return;
    navigating = true;
    show(false);
    try { sessionStorage.setItem(STORAGE_KEY, '1'); } catch {}
    const delay = reduceMotion.matches ? 40 : 320;
    window.setTimeout(() => { location.href = url; }, delay);
  };

  window.FPTPageTransition = { go, show, hide };

  document.addEventListener('click', (event) => {
    const anchor = event.target.closest?.('a[href]');
    if (!isSameSiteNavigation(anchor, event)) return;
    event.preventDefault();
    go(anchor.href);
  }, true);

  let arriving = false;
  try {
    arriving = sessionStorage.getItem(STORAGE_KEY) === '1';
    if (arriving) sessionStorage.removeItem(STORAGE_KEY);
  } catch {}

  if (arriving) {
    show(true);
    window.setTimeout(hide, reduceMotion.matches ? 70 : 260);
  }

  window.addEventListener('pageshow', (event) => {
    if (event.persisted) hide();
  });

  window.setTimeout(() => {
    if (overlay.classList.contains('is-active') && !navigating) hide();
  }, 1400);
})();