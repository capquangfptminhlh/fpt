const isGitHubPagesProject = location.hostname === 'capquangfptminhlh.github.io';
const siteBase = isGitHubPagesProject ? '/fpt' : '';
const sitePath = (path = '/') => `${siteBase}${path.startsWith('/') ? path : `/${path}`}`;

/* Load the dedicated phone design layer on every template. The homepage also
 * benefits from the same file, while desktop keeps the existing design system. */
if (!document.querySelector('link[data-mobile-v3]')) {
  const mobileStyles = document.createElement('link');
  mobileStyles.rel = 'stylesheet';
  mobileStyles.href = `${sitePath('/assets/css/mobile-v3.css')}?v=20260817-3`;
  mobileStyles.dataset.mobileV3 = 'true';
  document.head.appendChild(mobileStyles);
}

/* GitHub Pages project sites live below /fpt/. Normalize root-absolute internal
 * links so navigation never escapes to capquangfptminhlh.github.io/. */
if (siteBase) {
  document.querySelectorAll('a[href^="/"]').forEach((anchor) => {
    const href = anchor.getAttribute('href');
    if (!href || href === siteBase || href.startsWith(`${siteBase}/`)) return;
    anchor.setAttribute('href', sitePath(href));
  });
}

const toggle = document.querySelector('.mobile-toggle');
const navLinks = document.querySelector('.nav-links');

if (toggle && navLinks) {
  toggle.setAttribute('aria-expanded', 'false');

  const closeMenu = () => {
    navLinks.classList.remove('open');
    document.body.classList.remove('nav-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Mở menu');
  };

  toggle.addEventListener('click', (event) => {
    event.stopPropagation();
    const isOpen = navLinks.classList.toggle('open');
    document.body.classList.toggle('nav-open', isOpen);
    toggle.setAttribute('aria-expanded', String(isOpen));
    toggle.setAttribute('aria-label', isOpen ? 'Đóng menu' : 'Mở menu');
  });

  navLinks.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });

  document.addEventListener('click', (event) => {
    if (!navLinks.contains(event.target) && !toggle.contains(event.target)) closeMenu();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeMenu();
  });

  const menuBreakpoint = window.matchMedia('(max-width:1180px)');
  menuBreakpoint.addEventListener?.('change', (event) => {
    if (!event.matches) closeMenu();
  });
}

/* Mobile conversion shell: one persistent call action and one registration
 * action across all 73 static pages without duplicating markup in each file. */
const phoneViewport = window.matchMedia('(max-width:760px)');
let mobileCta = null;

const syncMobileCta = () => {
  if (!mobileCta) {
    mobileCta = document.createElement('nav');
    mobileCta.className = 'mobile-bottom-cta';
    mobileCta.setAttribute('aria-label', 'Liên hệ nhanh');
    mobileCta.innerHTML = `
      <a class="mobile-call" href="tel:19006600" aria-label="Gọi tổng đài 1900 6600">☎ Gọi ngay</a>
      <a class="mobile-register" href="${sitePath('/lien-he/')}" aria-label="Đăng ký tư vấn lắp mạng FPT">Đăng ký tư vấn</a>
    `;
    document.body.appendChild(mobileCta);
  }

  document.body.classList.toggle('has-mobile-cta', phoneViewport.matches);
  mobileCta.hidden = !phoneViewport.matches;
};

syncMobileCta();
phoneViewport.addEventListener?.('change', syncMobileCta);

const form = document.querySelector('#advisor-form');
if (form) {
  const map = {
    family: { id: 'giga', text: 'Gói GIGA phù hợp gia đình nhỏ, lướt web, xem phim HD và học tập online.' },
    game: { id: 'sky', text: 'Gói SKY phù hợp chơi game, ping ổn định và nhiều thiết bị hoạt động cùng lúc.' },
    camera: { id: 'meta', text: 'Gói META phù hợp nhà nhiều tầng, camera an ninh và hệ sinh thái smart home.' },
    office: { id: 'meta', text: 'Gói META phù hợp văn phòng nhỏ và không gian làm việc cường độ cao.' },
    cafe: { id: 'sky', text: 'Gói SKY phù hợp quán cafe cần kết nối ổn định cho nhiều khách cùng lúc.' }
  };

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const need = document.querySelector('#need')?.value || 'family';
    const result = document.querySelector('#advisor-result');
    const picked = map[need] || map.family;
    if (!result) return;

    result.innerHTML = `<div class="seo-box"><strong>Gợi ý nhanh:</strong> ${picked.text} <a href="${sitePath(`/goi-cuoc/${picked.id}/`)}" style="color:#1751c3;font-weight:800">Xem chi tiết →</a></div>`;
    result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });
}

/* Image routing supports both normal hosting at / and GitHub Pages at /fpt/. */
const imageRoot = sitePath('/assets/images/');
const seoRoot = `${imageRoot}seo/`;

const manualHeroMap = {
  '/lap-mang-fpt': `${seoRoot}ho-tro--lap-mang-fpt-mat-bao-lau-hero.webp`,
  '/internet-fpt': `${seoRoot}goi-cuoc-fpt-hero.webp`,
  '/internet-truyen-hinh-fpt': `${seoRoot}internet-truyen-hinh-fpt-hero.webp`,
  '/cap-quang-fpt': `${seoRoot}kien-thuc--ftth-la-gi-hero.webp`,
  '/wifi-fpt': `${seoRoot}mesh-wifi-fpt-hero.webp`,
  '/wifi-6-fpt': `${seoRoot}wifi-6-fpt-hero.webp`,
  '/wifi-7': `${seoRoot}so-sanh--wifi-6-vs-wifi-7-hero.webp`,
  '/mesh-wifi-fpt': `${seoRoot}mesh-wifi-fpt-hero.webp`,
  '/xgs-pon-fpt': `${seoRoot}xgs-pon-fpt-hero.webp`,
  '/camera-fpt': `${seoRoot}giai-phap--camera-hero.webp`,
  '/fpt-play': `${imageRoot}promo-fptplay.webp`,
  '/f-game-fpt': `${seoRoot}f-game-fpt-hero.webp`,
  '/goi-cuoc-fpt': `${seoRoot}goi-cuoc-fpt-hero.webp`,
  '/bang-gia-fpt': `${seoRoot}bang-gia-fpt-hero.webp`,
  '/speedx-fpt': `${seoRoot}speedx-fpt-hero.webp`,
  '/ho-tro': `${seoRoot}ho-tro-hero.webp`,
  '/giai-phap': `${seoRoot}giai-phap-hero.webp`,
  '/kien-thuc': `${seoRoot}kien-thuc-hero.webp`,
  '/so-sanh': `${seoRoot}so-sanh-hero.webp`,
  '/khu-vuc': `${seoRoot}khu-vuc-hero.webp`,
  '/goi-cuoc/giga': `${seoRoot}goi-cuoc-fpt-hero.webp`,
  '/goi-cuoc/sky': `${seoRoot}so-sanh--giga-vs-sky-hero.webp`,
  '/goi-cuoc/meta': `${seoRoot}xgs-pon-fpt-hero.webp`
};

const safeSwapImage = (element, nextSrc) => {
  if (!element || !nextSrc) return;
  const probe = new Image();
  probe.onload = () => {
    element.src = nextSrc;
    element.removeAttribute('srcset');
  };
  probe.src = nextSrc;
};

let runtimePath = location.pathname;
if (siteBase && runtimePath.startsWith(`${siteBase}/`)) runtimePath = runtimePath.slice(siteBase.length);
if (siteBase && runtimePath === siteBase) runtimePath = '/';
const currentPath = (`/${runtimePath.split('/').filter(Boolean).join('/')}`).replace(/\/$/, '') || '/';

const standardHero = document.querySelector('.subpage-hero .wrap > img');
const seoHero = document.querySelector('.seo-hero > img');

if (standardHero) {
  const mapped = manualHeroMap[currentPath];
  if (mapped) safeSwapImage(standardHero, mapped);
}

if (seoHero) {
  const mapped = manualHeroMap[currentPath];
  if (mapped) {
    safeSwapImage(seoHero, mapped);
  } else if (currentPath !== '/') {
    const slug = currentPath.slice(1).replaceAll('/', '--');
    safeSwapImage(seoHero, `${seoRoot}${slug}-hero.webp`);
  }
}

const packageImages = document.querySelectorAll('.package-media img');
const packageArtwork = [
  `${seoRoot}goi-cuoc-fpt-hero.webp`,
  `${seoRoot}so-sanh--giga-vs-sky-hero.webp`,
  `${seoRoot}xgs-pon-fpt-hero.webp`
];
packageImages.forEach((image, index) => safeSwapImage(image, packageArtwork[index]));

document.querySelectorAll('img').forEach((image) => {
  image.addEventListener('error', () => {
    image.classList.add('image-load-error');
  }, { once: true });
});