from __future__ import annotations

import argparse
from pathlib import Path

EXPECTED_PROVINCES = [
    'ha-noi','cao-bang','tuyen-quang','dien-bien','lai-chau','son-la','lao-cai','thai-nguyen',
    'lang-son','quang-ninh','bac-ninh','phu-tho','hai-phong','hung-yen','ninh-binh','thanh-hoa',
    'nghe-an','ha-tinh','quang-tri','hue','da-nang','quang-ngai','gia-lai','khanh-hoa','dak-lak',
    'lam-dong','dong-nai','thanh-pho-ho-chi-minh','tay-ninh','can-tho','vinh-long','dong-thap',
    'ca-mau','an-giang'
]

PLAN_IDS = (
    'giga-f1','giga-f2','giga-f3','sky-f1','sky-f2','sky-f3','meta-f1','meta-f2','meta-f3','fpt-an-tam','f-game-f1',
    'combo-giga-f1','combo-sky-f1','combo-sky-f2','combo-sky-f3','combo-meta-f1','combo-meta-f2','combo-meta-f3',
    'combo-giga-f2-lite','combo-giga-f3-lite','combo-meta-f1-lite','combo-meta-f2-lite','combo-f-game-f1',
    'camera-2-mix','camera-2-in','camera-2-out','camera-3-in','camera-3-out','camera-3-2in1out','camera-3-1in2out'
)

REQUIRED_MARKERS = (
    'data-current-offerings="30"','data-current-offerings-observed="2026-08-18"',
    'Internet GIGA F1','Internet SKY F3','Internet META F3','FPT An Tâm','Internet F‑Game F1',
    'Combo SKY F2 + FPT Play','Combo META F3 + FPT Play','Combo GIGA F2 Lite','Combo META F2 Lite','Combo F‑Game F1 + FPT Play',
    'Combo 2 Camera Trong + Ngoài','Combo 3 Camera – 1 Trong + 2 Ngoài',
    'https://fpt.vn/internet/ca-nhan','https://fpt.vn/internet/gia-dinh','https://fpt.vn/internet/goi-combo-f-game-f1','https://fpt.vn/camera'
)

FORBIDDEN_REGION_SPECIFIC_IDS = ('skyeyes3-f1-iq4s','skyeyes3-f2-iq4s','skyeyes3-f3-iq4s','triple-sky-camera-play4-tay-nam-bo')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    total = 0
    for slug in EXPECTED_PROVINCES:
        path = site / 'khu-vuc' / slug / 'index.html'
        if not path.exists():
            raise SystemExit(f'CURRENT OFFERINGS QA FAIL: missing {slug}')
        html = path.read_text(encoding='utf-8')
        if html.count('data-local-current-plan-card') != 30:
            raise SystemExit(f'CURRENT OFFERINGS QA FAIL: {slug} current plan count != 30')
        if html.count('data-current-plan-group="internet"') != 11:
            raise SystemExit(f'CURRENT OFFERINGS QA FAIL: {slug} internet extras != 11')
        if html.count('data-current-plan-group="combo"') != 12:
            raise SystemExit(f'CURRENT OFFERINGS QA FAIL: {slug} combo extras != 12')
        if html.count('data-current-plan-group="camera"') != 7:
            raise SystemExit(f'CURRENT OFFERINGS QA FAIL: {slug} camera extras != 7')
        for pid in PLAN_IDS:
            if f'data-current-plan-id="{pid}"' not in html:
                raise SystemExit(f'CURRENT OFFERINGS QA FAIL: {slug} missing {pid}')
        for marker in REQUIRED_MARKERS:
            if marker not in html:
                raise SystemExit(f'CURRENT OFFERINGS QA FAIL: {slug} missing marker {marker}')
        for pid in FORBIDDEN_REGION_SPECIFIC_IDS:
            if pid in html:
                raise SystemExit(f'CURRENT OFFERINGS QA FAIL: region-only plan leaked nationwide: {pid}')
        if html.count('data-select-current-plan=') != 30:
            raise SystemExit(f'CURRENT OFFERINGS QA FAIL: {slug} current CTA count != 30')
        total += 30
    print(f'CURRENT OFFERINGS QA PASS: 34/34 provinces × 30 additional current variants = {total}; total full package blocks = {34 * 56}; region-only Tây Nam Bộ variants excluded')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
