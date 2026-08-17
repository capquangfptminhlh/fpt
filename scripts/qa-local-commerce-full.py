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

REQUIRED = (
    'data-full-plan-details="true"','data-local-catalog-full-style="v2"',
    'local-plan-full-head','local-plan-full-metrics','local-plan-full-content',
    'local-plan-contract-grid','local-plan-benefit-list','local-plan-register',
    'Giá cước','VAT & chi phí khác','Thiết bị thực tế','Khuyến mãi','Hạ tầng','Ngày đối chiếu',
    'Đối chiếu nguồn FPT','data-select-local-plan='
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
        if html.count('class="local-plan-card local-plan-card-full"') != 26:
            raise SystemExit(f'LOCAL FULL PLAN QA FAIL: {slug} does not have 26 full package blocks')
        if html.count('local-plan-contract-grid') != 26:
            raise SystemExit(f'LOCAL FULL PLAN QA FAIL: {slug} missing contract/detail blocks')
        if html.count('local-plan-full-metrics') != 26:
            raise SystemExit(f'LOCAL FULL PLAN QA FAIL: {slug} missing metrics blocks')
        if html.count('local-plan-benefit-list') != 26:
            raise SystemExit(f'LOCAL FULL PLAN QA FAIL: {slug} missing benefit blocks')
        if html.count('data-select-local-plan=') != 26:
            raise SystemExit(f'LOCAL FULL PLAN QA FAIL: {slug} registration CTA count != 26')
        total += 26
    print(f'LOCAL FULL PLAN QA PASS: 34/34 provinces × 26 full package blocks = {total}; specs + benefits + conditions + registration flow present')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
