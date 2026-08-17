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

BASE_COUNT = 26
CURRENT_EXTRA_COUNT = 30
TOTAL_COUNT = BASE_COUNT + CURRENT_EXTRA_COUNT

REQUIRED = (
    'data-full-plan-details="true"','data-local-catalog-full-style="v2"',
    'local-plan-full-head','local-plan-full-metrics','local-plan-full-content',
    'local-plan-contract-grid','local-plan-benefit-list','local-plan-register',
    'Giá cước','VAT & chi phí khác','Thiết bị thực tế','Khuyến mãi','Hạ tầng','Ngày đối chiếu',
    'Nguồn sản phẩm:','data-select-local-plan=','data-current-offerings="30"'
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    css = site / 'assets/css/local-catalog-full.css'
    if not css.exists() or css.stat().st_size < 3000:
        raise SystemExit('LOCAL FULL PLAN QA FAIL: full catalog CSS missing or too small')
    total = 0
    for slug in EXPECTED:
        path = site / 'khu-vuc' / slug / 'index.html'
        if not path.exists():
            raise SystemExit(f'LOCAL FULL PLAN QA FAIL: missing province {slug}')
        html = path.read_text(encoding='utf-8')
        for marker in REQUIRED:
            if marker not in html:
                raise SystemExit(f'LOCAL FULL PLAN QA FAIL: {slug} missing {marker}')
        if html.count('class="local-plan-card local-plan-card-full"') != BASE_COUNT:
            raise SystemExit(f'LOCAL FULL PLAN QA FAIL: {slug} base full package blocks != {BASE_COUNT}')
        if html.count('data-local-current-plan-card') != CURRENT_EXTRA_COUNT:
            raise SystemExit(f'LOCAL FULL PLAN QA FAIL: {slug} current extra blocks != {CURRENT_EXTRA_COUNT}')
        for marker in ('local-plan-contract-grid','local-plan-full-metrics','local-plan-benefit-list','local-plan-register'):
            if html.count(marker) != TOTAL_COUNT:
                raise SystemExit(f'LOCAL FULL PLAN QA FAIL: {slug} {marker} count != {TOTAL_COUNT}')
        if html.count('data-select-local-plan=') != BASE_COUNT:
            raise SystemExit(f'LOCAL FULL PLAN QA FAIL: {slug} base registration CTA count != {BASE_COUNT}')
        if html.count('data-select-current-plan=') != CURRENT_EXTRA_COUNT:
            raise SystemExit(f'LOCAL FULL PLAN QA FAIL: {slug} current registration CTA count != {CURRENT_EXTRA_COUNT}')
        total += TOTAL_COUNT
    print(f'LOCAL FULL PLAN QA PASS: 34/34 provinces × {TOTAL_COUNT} full package blocks = {total}; specs + benefits + conditions + registration flow present')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
