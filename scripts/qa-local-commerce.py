from __future__ import annotations

import argparse
from pathlib import Path

EXPECTED = [
    'ha-noi','cao-bang','tuyen-quang','dien-bien','lai-chau','son-la','lao-cai','thai-nguyen',
    'lang-son','quang-ninh','bac-ninh','phu-tho','hai-phong','hung-yen','ninh-binh','thanh-hoa',
    'nghe-an','ha-tinh','quang-tri','hue','da-nang','quang-ngai','gia-lai','khanh-hoa','dak-lak',
    'lam-dong','dong-nai','thanh-pho-ho-chi-minh','tay-ninh','can-tho','vinh-long','dong-thap',
    'ca-mau','an-giang'
]

REQUIRED_PLAN_IDS = (
    'giga','sky','meta','f-game','speedx2','speedx2-pro','speedx10','speedx10-pro',
    'combo-giga','combo-sky','combo-meta','combo-f-game','fpt-play','sports-sky','sports-meta',
    'camera-fpt','play3','play4','iq4s','camera-2','camera-3','camera-5',
    'gigaeyes-play4','skyeyes-play4','triple-gigaeyes','triple-skyeyes'
)

REQUIRED_VERIFIED_MARKERS = (
    '195.000đ/tháng','295.000đ/tháng','225.000đ/tháng','999.000đ/tháng',
    '1.099.000đ/tháng','1.599.000đ/tháng','1.690.000đ/tháng',
    '300 / 300 Mbps','1 Gbps / 300 Mbps','1 Gbps / 1 Gbps','2 Gbps / 2 Gbps','10 Gbps / 10 Gbps',
    '200.000đ/tháng','209.000đ/tháng','320.000đ/tháng','270.000đ/tháng',
    '269.000đ/tháng','369.000đ/tháng','510.000đ','950.000đ','1.150.000đ','2.100.000đ',
    '220.000đ/tháng','245.000đ/tháng',
    'https://fpt.vn/lap-wifi','https://fpt.vn/internet/game-thu',
    'https://fpt.vn/internet/speed-x2-pro','https://fpt.vn/internet/speed-x10-pro','https://fpt.vn/camera'
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    css = site / 'assets' / 'css' / 'local-catalog.css'
    if not css.exists() or css.stat().st_size < 1500:
        raise SystemExit('LOCAL COMMERCE QA FAIL: local-catalog.css missing or suspiciously small')

    for slug in EXPECTED:
        path = site / 'khu-vuc' / slug / 'index.html'
        if not path.exists():
            raise SystemExit(f'LOCAL COMMERCE QA FAIL: missing landing {slug}')
        html = path.read_text(encoding='utf-8')
        if 'class="section local-commerce"' not in html:
            raise SystemExit(f'LOCAL COMMERCE QA FAIL: {slug} missing rich commerce section')
        if 'data-catalog-observed="2026-08-18"' not in html:
            raise SystemExit(f'LOCAL COMMERCE QA FAIL: {slug} missing catalog observation date')
        if 'data-local-catalog-style="v1"' not in html:
            raise SystemExit(f'LOCAL COMMERCE QA FAIL: {slug} missing local catalog stylesheet')
        if html.count('data-local-plan-card') != 26:
            raise SystemExit(f'LOCAL COMMERCE QA FAIL: {slug} product card count != 26')
        expected_counts = {
            'internet': 8,
            'play': 5,
            'play-extra': 2,
            'camera': 3,
            'camera-extra': 4,
            'camera-bundle': 4,
        }
        for kind, count in expected_counts.items():
            actual = html.count(f'data-local-product="{kind}"')
            if actual != count:
                raise SystemExit(f'LOCAL COMMERCE QA FAIL: {slug} {kind} count={actual}, expected={count}')
        for plan_id in REQUIRED_PLAN_IDS:
            if f'data-plan-id="{plan_id}"' not in html:
                raise SystemExit(f'LOCAL COMMERCE QA FAIL: {slug} missing plan {plan_id}')
        for marker in REQUIRED_VERIFIED_MARKERS:
            if marker not in html:
                raise SystemExit(f'LOCAL COMMERCE QA FAIL: {slug} missing verified marker {marker}')
        if html.count('data-select-local-plan=') != 26:
            raise SystemExit(f'LOCAL COMMERCE QA FAIL: {slug} registration CTA count != 26')
        for marker in (
            'Các mức “chỉ từ” dưới đây được đối chiếu từ website FPT Telecom',
            'có thể thay đổi theo khu vực và thời điểm',
            'báo giá cuối cùng chỉ được xác nhận sau khi kiểm tra địa chỉ',
            'data-local-news-link',
            'href="tin-tuc/"',
        ):
            if marker not in html:
                raise SystemExit(f'LOCAL COMMERCE QA FAIL: {slug} missing safety/UX marker {marker}')

    print('LOCAL COMMERCE QA PASS: 34/34 provinces × 26 product cards = 884 cards; prices/speeds sourced, disclaimer + CTA + responsive CSS present')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
