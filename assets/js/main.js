const toggle = document.querySelector('.mobile-toggle');
const navLinks = document.querySelector('.nav-links');

if (toggle && navLinks) {
  toggle.setAttribute('aria-expanded', 'false');

  const closeMenu = () => {
    navLinks.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
  };

  toggle.addEventListener('click', (event) => {
    event.stopPropagation();
    const isOpen = navLinks.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(isOpen));
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
}

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

    result.innerHTML = `<div class="seo-box"><strong>Gợi ý nhanh:</strong> ${picked.text} <a href="/goi-cuoc/${picked.id}/" style="color:#1751c3;font-weight:800">Xem chi tiết →</a></div>`;
    result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });
}

/*
 * Image routing
 * The repository already contains a large unique SEO image library. Older core
 * templates reused hero-family.webp or the same promo art on multiple pages.
 * This router upgrades visible imagery without changing canonical/SEO markup.
 */
const imageRoot = '/assets/images/';
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

const currentPath = (`/${location.pathname.split('/').filter(Boolean).join('/')}`).replace(/\/$/, '') || '/';
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

/* Give the three homepage package cards distinct, relevant images. */
const packageImages = document.querySelectorAll('.package-media img');
const packageArtwork = [
  `${seoRoot}goi-cuoc-fpt-hero.webp`,
  `${seoRoot}so-sanh--giga-vs-sky-hero.webp`,
  `${seoRoot}xgs-pon-fpt-hero.webp`
];
packageImages.forEach((image, index) => safeSwapImage(image, packageArtwork[index]));

/* Images should never take down a layout if an asset is missing. */
document.querySelectorAll('img').forEach((image) => {
  image.addEventListener('error', () => {
    image.classList.add('image-load-error');
  }, { once: true });
});
