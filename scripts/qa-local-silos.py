from __future__ import annotations

import argparse
import re
from html import unescape
from pathlib import Path

EXPECTED = [
    'ha-noi','cao-bang','tuyen-quang','dien-bien','lai-chau','son-la','lao-cai','thai-nguyen',
    'lang-son','quang-ninh','bac-ninh','phu-tho','hai-phong','hung-yen','ninh-binh','thanh-hoa',
    'nghe-an','ha-tinh','quang-tri','hue','da-nang','quang-ngai','gia-lai','khanh-hoa','dak-lak',
    'lam-dong','dong-nai','thanh-pho-ho-chi-minh','tay-ninh','can-tho','vinh-long','dong-thap',
    'ca-mau','an-giang'
]


def capture(pattern: str, html: str, label: str, path: Path) -> str:
    match = re.search(pattern, html, flags=re.I | re.S)
    if not match:
        raise SystemExit(f'LOCAL SILO QA FAIL: missing {label}: {path}')
    return re.sub(r'\s+', ' ', unescape(match.group(1))).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    root = site / 'khu-vuc'
    hub = root / 'index.html'
    if not hub.exists():
        raise SystemExit('LOCAL SILO QA FAIL: missing khu-vuc hub')
    hub_html = hub.read_text(encoding='utf-8')

    news_titles, news_h1s, news_canonicals = set(), set(), set()
    for slug in EXPECTED:
        landing = root / slug / 'index.html'
        news = root / slug / 'tin-tuc' / 'index.html'
        if not landing.exists():
            raise SystemExit(f'LOCAL SILO QA FAIL: missing landing {slug}')
        if not news.exists():
            raise SystemExit(f'LOCAL SILO QA FAIL: missing news hub {slug}')

        landing_html = landing.read_text(encoding='utf-8')
        if 'id="goi-dich-vu-dia-phuong"' not in landing_html:
            raise SystemExit(f'LOCAL SILO QA FAIL: {slug} missing service catalog')
        if landing_html.count('data-local-product="internet"') != 8:
            raise SystemExit(f'LOCAL SILO QA FAIL: {slug} internet catalog count != 8')
        if landing_html.count('data-local-product="play"') != 5:
            raise SystemExit(f'LOCAL SILO QA FAIL: {slug} FPT Play catalog count != 5')
        if landing_html.count('data-local-product="camera"') != 3:
            raise SystemExit(f'LOCAL SILO QA FAIL: {slug} camera catalog count != 3')
        if 'data-local-news-link' not in landing_html or 'href="tin-tuc/"' not in landing_html:
            raise SystemExit(f'LOCAL SILO QA FAIL: {slug} missing local news link')

        required_product_links = (
            '../../goi-cuoc/giga/', '../../goi-cuoc/sky/', '../../goi-cuoc/meta/', '../../goi-cuoc/f-game/',
            '../../goi-cuoc/speedx2/', '../../goi-cuoc/speedx2-pro/', '../../goi-cuoc/speedx10/', '../../goi-cuoc/speedx10-pro/',
            '../../goi-cuoc/combo-giga/', '../../goi-cuoc/combo-sky/', '../../goi-cuoc/combo-meta/', '../../goi-cuoc/combo-f-game/',
            '../../fpt-play/', '../../camera-fpt/', '../../camera-fpt/play-3/', '../../camera-fpt/play-4/'
        )
        for link in required_product_links:
            if link not in landing_html:
                raise SystemExit(f'LOCAL SILO QA FAIL: {slug} missing product link {link}')

        news_html = news.read_text(encoding='utf-8')
        title = capture(r'<title>(.*?)</title>', news_html, 'news title', news)
        h1 = capture(r'<h1[^>]*>(.*?)</h1>', news_html, 'news h1', news)
        canonical = capture(r'<link\b[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', news_html, 'news canonical', news)
        if f'/fpt/khu-vuc/{slug}/tin-tuc/' not in canonical:
            raise SystemExit(f'LOCAL SILO QA FAIL: wrong news canonical for {slug}: {canonical}')
        news_titles.add(title); news_h1s.add(h1); news_canonicals.add(canonical)

        for marker in (
            'Khả năng triển khai, thiết bị và ưu đãi phụ thuộc hạ tầng thực tế.',
            'data-contact-dock-script=', 'data-ui-reset-style=', 'data-ui-motion-style=', 'data-page-transition-script=',
            '../../../fpt-play/', '../../../camera-fpt/', '../#goi-dich-vu-dia-phuong'
        ):
            if marker not in news_html:
                raise SystemExit(f'LOCAL SILO QA FAIL: {slug} news missing marker {marker}')
        if re.search(r'\b\d{2,4}(?:[.,]\d{3})+\s*(?:đ|vnđ|vnd|đồng)', news_html, flags=re.I):
            raise SystemExit(f'LOCAL SILO QA FAIL: unsupported numeric price claim in news {slug}')
        if re.search(r'\b\d+\s*(?:mbps|gbps)\b', news_html, flags=re.I):
            raise SystemExit(f'LOCAL SILO QA FAIL: unsupported numeric speed claim in news {slug}')
        if f'{slug}/tin-tuc/' not in hub_html:
            raise SystemExit(f'LOCAL SILO QA FAIL: hub missing news link {slug}')

    if len(news_titles) != 34 or len(news_h1s) != 34 or len(news_canonicals) != 34:
        raise SystemExit(
            f'LOCAL SILO QA FAIL: news uniqueness titles={len(news_titles)} h1={len(news_h1s)} canonicals={len(news_canonicals)}'
        )

    nav_pages = 0
    for path in site.rglob('*.html'):
        html = path.read_text(encoding='utf-8')
        nav = re.search(r'<nav\b[^>]*class=["\'][^"\']*nav-links[^"\']*["\'][^>]*>(.*?)</nav>', html, flags=re.I | re.S)
        if not nav:
            continue
        nav_pages += 1
        if not re.search(r'>\s*Khu vực\s*</a>', nav.group(1), flags=re.I):
            raise SystemExit(f'LOCAL SILO QA FAIL: Khu vực nav missing in {path.relative_to(site)}')

    if nav_pages < 100:
        raise SystemExit(f'LOCAL SILO QA FAIL: suspicious nav page count {nav_pages}')

    print(
        f'LOCAL SILO QA PASS: 34/34 service catalogs, 34/34 news hubs, '
        f'8 internet + 5 FPT Play/combo + 3 camera links per province; Khu vực nav pages={nav_pages}'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
