from __future__ import annotations

import argparse
import re
from pathlib import Path

EXPECTED = [
    'ha-noi','cao-bang','tuyen-quang','dien-bien','lai-chau','son-la','lao-cai','thai-nguyen',
    'lang-son','quang-ninh','bac-ninh','phu-tho','hai-phong','hung-yen','ninh-binh','thanh-hoa',
    'nghe-an','ha-tinh','quang-tri','hue','da-nang','quang-ngai','gia-lai','khanh-hoa','dak-lak',
    'lam-dong','dong-nai','thanh-pho-ho-chi-minh','tay-ninh','can-tho','vinh-long','dong-thap','ca-mau','an-giang'
]
EXPECTED_CARDS = 103
EXPECTED_INTERNAL = 26


def commerce(html: str, slug: str) -> str:
    match = re.search(r'<section\b(?=[^>]*\blocal-commerce\b)[^>]*>.*?</section>', html, flags=re.I | re.S)
    if not match:
        raise SystemExit(f'PREMIUM CATALOG QA FAIL: {slug} commerce section missing')
    return match.group(0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    css = site / 'assets/css/local-catalog-premium.css'
    js = site / 'assets/js/local-catalog-premium.js'
    if not css.exists() or css.stat().st_size < 7000:
        raise SystemExit('PREMIUM CATALOG QA FAIL: premium CSS missing or unexpectedly small')
    if not js.exists() or js.stat().st_size < 900:
        raise SystemExit('PREMIUM CATALOG QA FAIL: premium JS missing or unexpectedly small')
    css_text = css.read_text(encoding='utf-8')
    for marker in ('grid-template-columns:repeat(3,minmax(0,1fr))', '.premium-plan-card', '.premium-plan-actions', '.premium-plan-more', '@media(max-width:760px)'):
        if marker not in css_text:
            raise SystemExit(f'PREMIUM CATALOG QA FAIL: CSS missing {marker}')

    total = 0
    internal_detail_links = 0
    for slug in EXPECTED:
        path = site / 'khu-vuc' / slug / 'index.html'
        if not path.exists():
            raise SystemExit(f'PREMIUM CATALOG QA FAIL: missing province {slug}')
        html = path.read_text(encoding='utf-8')
        block = commerce(html, slug)
        if 'data-premium-catalog="v4"' not in block:
            raise SystemExit(f'PREMIUM CATALOG QA FAIL: {slug} missing premium catalog v4 marker')
        if 'data-local-catalog-premium-style="v4"' not in html or 'data-local-catalog-premium-script="v4"' not in html:
            raise SystemExit(f'PREMIUM CATALOG QA FAIL: {slug} premium v4 assets not injected')
        checks = {
            'cards': block.count('data-premium-plan-card'),
            'toggles': block.count('data-premium-plan-toggle'),
            'cta': block.count('data-premium-select-plan'),
            'speed': block.count('class="premium-plan-speed"'),
            'benefits': block.count('class="premium-plan-benefits"'),
            'drawers': block.count('class="premium-plan-drawer"'),
        }
        for label, count in checks.items():
            if count != EXPECTED_CARDS:
                raise SystemExit(f'PREMIUM CATALOG QA FAIL: {slug} {label}={count}, expected={EXPECTED_CARDS}')
        links = re.findall(r'<a class="premium-plan-more" href="([^"]+)">', block, flags=re.I)
        if len(links) != EXPECTED_INTERNAL:
            raise SystemExit(f'PREMIUM CATALOG QA FAIL: {slug} internal package detail links != {EXPECTED_INTERNAL}')
        if any(not href.startswith(('../', './')) or 'fpt.vn' in href.lower() for href in links):
            raise SystemExit(f'PREMIUM CATALOG QA FAIL: {slug} premium detail link is not internal')
        if 'local-plan-card-full' in block or 'local-plan-full-head' in block or 'local-plan-contract-grid' in block:
            raise SystemExit(f'PREMIUM CATALOG QA FAIL: {slug} legacy rich-card markup still visible')
        lowered = block.lower()
        if 'fpt.vn' in lowered or 'nguồn fpt' in lowered or 'source of truth' in lowered:
            raise SystemExit(f'PREMIUM CATALOG QA FAIL: {slug} visible source/reference text leaked into catalog')
        if 'Giá & ưu đãi theo địa chỉ' not in block:
            raise SystemExit(f'PREMIUM CATALOG QA FAIL: {slug} commercial verification note missing')
        for pid in ('lux500','super800-biz-plus','combo-giga-vvip','fpt-play-premium','sky-antam7-play4-one','speedx10-pro-iq4s'):
            if f'data-premium-plan-id="{pid}"' not in block:
                raise SystemExit(f'PREMIUM CATALOG QA FAIL: {slug} representative official offer {pid} missing')
        total += EXPECTED_CARDS
        internal_detail_links += len(links)

    print(f'PREMIUM CATALOG QA PASS: 34/34 provinces × {EXPECTED_CARDS} premium offers = {total}; 3-column desktop + 2/1 responsive; compact fronts + inline details + CTA; no visible source links; internal package detail links={internal_detail_links}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
