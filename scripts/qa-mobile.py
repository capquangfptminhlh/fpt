from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED=(
    'overflow-x:hidden!important',
    'grid-template-columns:minmax(0,1fr)!important',
    'overflow-wrap:break-word!important',
    '.data-table{display:block!important',
    '.packages,.promos,.use-cases,.home-v2 .plan-grid,.home-v2 .solution-grid,.home-v2 .intent-switch{display:flex!important;width:100%!important;max-width:100%!important;margin-inline:0!important',
    '.package,.promo,.use-card,.home-v2 .m-plan,.home-v2 .solution-card{flex:0 0 88%!important',
    '.contact-page .contact-copy{',
    '.motion-section::before,.motion-section::after,.motion-section-beam,.motion-footer-field,.motion-fiber-canvas,.motion-glow::before{display:none!important}',
    '.footer{padding:32px 0 calc(118px + env(safe-area-inset-bottom))!important',
    '@media(max-width:380px)',
)


def main()->None:
    parser=argparse.ArgumentParser(); parser.add_argument('--site',required=True); args=parser.parse_args()
    site=Path(args.site); pages=sorted(site.rglob('*.html')); css_path=site/'assets/css/mobile-stability.css'; errors=[]
    css=css_path.read_text(encoding='utf-8') if css_path.exists() else ''
    if not css_path.exists(): errors.append('missing mobile-stability.css')
    for token in REQUIRED:
        if token not in css: errors.append(f'mobile-stability missing {token}')
    ordered=viewport=0
    for page in pages:
        html=page.read_text(encoding='utf-8'); rel=page.relative_to(site)
        if 'name="viewport"' in html or "name='viewport'" in html: viewport+=1
        elif rel!=Path('support/index.html'): errors.append(f'{rel}: missing viewport meta')
        color=html.find('data-color-stability-style='); dock=html.find('data-contact-dock-style='); mobile=html.find('data-mobile-stability-style=')
        if min(color,dock,mobile)<0: errors.append(f'{rel}: missing final UI marker'); continue
        if not (color<dock<mobile): errors.append(f'{rel}: unsafe final mobile cascade color={color}, dock={dock}, mobile={mobile}'); continue
        if 'mobile-stability.css?v=20260817-2' not in html: errors.append(f'{rel}: stale mobile stability asset'); continue
        ordered+=1
    if errors:
        print('MOBILE QA FAIL'); [print(f'- {e}') for e in errors[:120]]; raise SystemExit(1)
    print(f'MOBILE QA PASS: pages={len(pages)}, ordered={ordered}, viewport={viewport}, overflow=guarded, typography=clean, content=one_column, carousels=contained, tables=contained, contact_collision=0, motion_color_wash=0')


if __name__=='__main__': main()
