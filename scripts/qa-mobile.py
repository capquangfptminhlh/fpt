from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED = (
    'html,body{width:100%;max-width:100%;overflow-x:clip!important}',
    'grid-template-columns:minmax(0,1fr)!important',
    'overflow-wrap:break-word!important',
    '.data-table{display:block!important',
    '.home-v2 .m-actions,.home-v2 .process,.home-v2 .trust-points',
    '.motion-section::before{inset:4px 0!important',
    '.motion-fiber-canvas{max-width:100%!important;opacity:.14!important',
    'body.has-contact-dock{padding-bottom:calc(102px + env(safe-area-inset-bottom))!important',
    '@media(max-width:380px)',
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    pages = sorted(site.rglob('*.html'))
    css_path = site / 'assets/css/mobile-stability.css'
    css = css_path.read_text(encoding='utf-8') if css_path.exists() else ''
    errors: list[str] = []

    if not css_path.exists():
        errors.append('Missing assets/css/mobile-stability.css')
    for token in REQUIRED:
        if token not in css:
            errors.append(f'mobile-stability.css missing: {token}')

    ordered = viewport = 0
    for page in pages:
        html = page.read_text(encoding='utf-8')
        rel = page.relative_to(site)
        if 'name="viewport"' in html or "name='viewport'" in html:
            viewport += 1
        elif rel != Path('support/index.html'):
            errors.append(f'{rel}: missing viewport meta')

        color = html.find('data-color-stability-style=')
        mobile = html.find('data-mobile-stability-style=')
        dock = html.find('data-contact-dock-style=')
        if min(color, mobile, dock) < 0:
            errors.append(f'{rel}: missing color/mobile/contact global style marker')
            continue
        if not (color < mobile < dock):
            errors.append(f'{rel}: unsafe mobile cascade order color={color}, mobile={mobile}, dock={dock}')
            continue
        if 'mobile-stability.css?v=20260817-1' not in html:
            errors.append(f'{rel}: missing mobile stability v1')
            continue
        ordered += 1

    if errors:
        print('MOBILE QA FAIL')
        for item in errors[:120]:
            print(f'- {item}')
        raise SystemExit(1)

    print(
        f'MOBILE QA PASS: pages={len(pages)}, ordered={ordered}, viewport={viewport}, '
        'horizontal_overflow_guard=ready, readable_wrap=ready, one_column_content=ready, '
        'swipe_cards=bounded, table_scroll=ready, motion_bounds=ready, dock_clearance=ready'
    )


if __name__ == '__main__':
    main()
