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
BAD_SLUGS = ('/khu-vuc/a-nang/','/khu-vuc/ak-lak/','/khu-vuc/ien-bien/','/khu-vuc/ong-nai/','/khu-vuc/ong-thap/')


def text_words(html: str) -> int:
    clean = re.sub(r'<script\b.*?</script>|<style\b.*?</style>', ' ', html, flags=re.I | re.S)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    clean = unescape(clean)
    return len(re.findall(r'\b[\wÀ-ỹ]+\b', clean, flags=re.U))


def capture(pattern: str, html: str, label: str, path: Path) -> str:
    match = re.search(pattern, html, flags=re.I | re.S)
    if not match:
        raise SystemExit(f'LOCAL QA FAIL: missing {label}: {path}')
    return re.sub(r'\s+', ' ', unescape(match.group(1))).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    hub = site / 'khu-vuc' / 'index.html'
    if not hub.exists():
        raise SystemExit('LOCAL QA FAIL: missing khu-vuc/index.html')
    hub_html = hub.read_text(encoding='utf-8')

    actual = sorted(p.parent.name for p in (site / 'khu-vuc').glob('*/index.html'))
    if sorted(EXPECTED) != actual:
        missing = sorted(set(EXPECTED) - set(actual))
        extra = sorted(set(actual) - set(EXPECTED))
        raise SystemExit(f'LOCAL QA FAIL: expected 34 local pages; missing={missing}, extra={extra}')

    titles, h1s, canonicals = set(), set(), set()
    for slug in EXPECTED:
        path = site / 'khu-vuc' / slug / 'index.html'
        html = path.read_text(encoding='utf-8')
        title = capture(r'<title>(.*?)</title>', html, 'title', path)
        h1 = capture(r'<h1[^>]*>(.*?)</h1>', html, 'h1', path)
        canonical = capture(r'<link\b[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', html, 'canonical', path)
        if f'/fpt/khu-vuc/{slug}/' not in canonical:
            raise SystemExit(f'LOCAL QA FAIL: wrong canonical for {slug}: {canonical}')
        canonicals.add(canonical); titles.add(title); h1s.add(h1)
        required = (
            'data-lead-form', 'lead-form.js', 'data-contact-dock-script=', 'data-ui-reset-style=',
            'data-ui-motion-style=', 'data-page-transition-script=', 'xaydungchinhsach.chinhphu.vn',
            'Khả năng triển khai, thiết bị và ưu đãi phụ thuộc hạ tầng thực tế.',
            'Giá, hạ tầng, thiết bị và ưu đãi cần được xác nhận lại theo địa chỉ.'
        )
        for marker in required:
            if marker not in html:
                raise SystemExit(f'LOCAL QA FAIL: {slug} missing marker: {marker}')
        if text_words(html) < 650:
            raise SystemExit(f'LOCAL QA FAIL: {slug} too thin ({text_words(html)} words)')
        if re.search(r'\b\d{2,4}(?:[.,]\d{3})+\s*(?:đ|vnđ|vnd|đồng)', html, flags=re.I):
            raise SystemExit(f'LOCAL QA FAIL: unsupported numeric price claim in {slug}')
        if re.search(r'\b\d+\s*(?:mbps|gbps)\b', html, flags=re.I):
            raise SystemExit(f'LOCAL QA FAIL: unsupported numeric speed claim in {slug}')
        if f'{slug}/' not in hub_html:
            raise SystemExit(f'LOCAL QA FAIL: hub missing link to {slug}')

    if len(titles) != 34 or len(h1s) != 34 or len(canonicals) != 34:
        raise SystemExit(f'LOCAL QA FAIL: uniqueness titles={len(titles)} h1={len(h1s)} canonicals={len(canonicals)}')
    combined = hub_html + ''.join((site / 'khu-vuc' / s / 'index.html').read_text(encoding='utf-8') for s in EXPECTED)
    for bad in BAD_SLUGS:
        if bad in combined:
            raise SystemExit(f'LOCAL QA FAIL: legacy broken slug leaked: {bad}')

    print('LOCAL QA PASS: 34/34 pages; unique title/H1/canonical; form + contact dock + UI motion + transition present; no unsupported numeric price/speed claims')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
