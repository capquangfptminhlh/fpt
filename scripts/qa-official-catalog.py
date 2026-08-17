from __future__ import annotations

import argparse
import re
from pathlib import Path

EXPECTED_SLUGS = [
    'ha-noi','cao-bang','tuyen-quang','dien-bien','lai-chau','son-la','lao-cai','thai-nguyen',
    'lang-son','quang-ninh','bac-ninh','phu-tho','hai-phong','hung-yen','ninh-binh','thanh-hoa',
    'nghe-an','ha-tinh','quang-tri','hue','da-nang','quang-ngai','gia-lai','khanh-hoa','dak-lak',
    'lam-dong','dong-nai','thanh-pho-ho-chi-minh','tay-ninh','can-tho','vinh-long','dong-thap','ca-mau','an-giang'
]
BASE = 56
ADDED = 47
TOTAL = BASE + ADDED
GROUP_COUNTS = {'official-play': 13, 'business': 12, 'camera-current': 7, 'wifi7-current': 15}
CORRECTED_PRICES = {
    'camera-fpt': 'Từ 500.000đ', 'play4': 'Từ 500.000đ', 'iq4s': 'Từ 500.000đ',
    'camera-2': 'Từ 1.000.000đ', 'camera-3': 'Từ 1.500.000đ', 'camera-5': 'Từ 2.500.000đ',
    'camera-2-mix': 'Từ 1.000.000đ', 'camera-2-in': 'Từ 1.000.000đ', 'camera-2-out': 'Từ 1.000.000đ',
    'camera-3-in': 'Từ 1.500.000đ', 'camera-3-out': 'Từ 1.500.000đ',
    'camera-3-2in1out': 'Từ 1.500.000đ', 'camera-3-1in2out': 'Từ 1.500.000đ',
}
REQUIRED_IDS = [
    'combo-giga-vvip','combo-sky-vvip','combo-meta-vvip','combo-lux500-vvip','combo-lux800-vvip',
    'combo-speedx2-vvip','combo-speedx10-vvip','vvip-1','vvip-2','fpt-play-cine','fpt-play-premium',
    'combo-an-tam','combo-giai-tri','lux500','lux800','super300-biz','super800-biz-plus',
    'giga-antam7-play4-multi','sky-antam7-iq4s-one','triple-sky-antam7-play4',
    'speedx2-play4','speedx2-iq4s','speedx2-pro-play4','speedx2-pro-iq4s','speedx2-eyes3-iq4s',
    'speedx2-eyes3-play4','speedx2-eyes3-play3','speedx2-pro-lite','speedx10-play4','speedx10-iq4s',
    'speedx10-pro-play4','speedx10-pro-iq4s','speedx10-eyes3-iq4s','speedx10-eyes3-play4','speedx10-pro-lite'
]


def commerce(html: str, slug: str) -> str:
    match = re.search(r'<section\b(?=[^>]*\blocal-commerce\b)[^>]*>.*?</section>', html, flags=re.I | re.S)
    if not match:
        raise SystemExit(f'OFFICIAL CATALOG QA FAIL: {slug} commerce missing')
    return match.group(0)


def article_for(block: str, pid: str) -> str:
    match = re.search(
        rf'<article\b(?=[^>]*(?:data-plan-id|data-current-plan-id)=["\']{re.escape(pid)}["\'])[^>]*>.*?</article>',
        block, flags=re.I | re.S,
    )
    return match.group(0) if match else ''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    aggregate = 0
    for slug in EXPECTED_SLUGS:
        path = site / 'khu-vuc' / slug / 'index.html'
        if not path.exists():
            raise SystemExit(f'OFFICIAL CATALOG QA FAIL: missing {slug}')
        html = path.read_text(encoding='utf-8')
        block = commerce(html, slug)
        rich = len(re.findall(r'<article\b[^>]*\blocal-plan-card-full\b', block, flags=re.I))
        if rich != TOTAL:
            raise SystemExit(f'OFFICIAL CATALOG QA FAIL: {slug} rich offers={rich}, expected={TOTAL}')
        if block.count('data-official-extra-plan-card') != ADDED:
            raise SystemExit(f'OFFICIAL CATALOG QA FAIL: {slug} official additions != {ADDED}')
        if f'data-official-extra-catalog="{ADDED}"' not in block:
            raise SystemExit(f'OFFICIAL CATALOG QA FAIL: {slug} official catalog marker missing')
        for group, expected in GROUP_COUNTS.items():
            group_match = re.search(rf'<div class="local-plan-group official-extra-group" data-official-extra-group="{group}">(.*?)</div>\s*</div>', block, flags=re.I | re.S)
            count = len(re.findall(rf'data-current-plan-group="{group}"', block, flags=re.I))
            if count != expected:
                raise SystemExit(f'OFFICIAL CATALOG QA FAIL: {slug} group {group}={count}, expected={expected}')
        for pid in REQUIRED_IDS:
            if not article_for(block, pid):
                raise SystemExit(f'OFFICIAL CATALOG QA FAIL: {slug} missing {pid}')
        for pid, price in CORRECTED_PRICES.items():
            article = article_for(block, pid)
            if not article or price not in article:
                raise SystemExit(f'OFFICIAL CATALOG QA FAIL: {slug} stale/missing price for {pid}')
        extra_match = re.search(r'<div class="official-extra-catalog".*?<div class="local-catalog-source">', block, flags=re.I | re.S)
        extra = extra_match.group(0) if extra_match else block
        if 'Áp dụng cho khu vực Tây Nam Bộ' in extra or 'Tây Nam Bộ-only' in extra:
            raise SystemExit(f'OFFICIAL CATALOG QA FAIL: {slug} region-only offer leaked')
        if '2026-08-18' not in block:
            raise SystemExit(f'OFFICIAL CATALOG QA FAIL: {slug} observed date missing')
        aggregate += rich
    print(f'OFFICIAL CATALOG QA PASS: 34/34 provinces × {TOTAL} rich offers = {aggregate}; additions={ADDED}/province (FPT Play/V.VIP + business + An Tâm 7 + Wi-Fi 7); camera snapshot prices corrected; Tây Nam Bộ-only variants excluded')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
