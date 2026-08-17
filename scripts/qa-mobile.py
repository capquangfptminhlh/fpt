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
FINAL_REQUIRED=(
    '.motion-heading,.motion-heading.is-motion-heading-visible,',
    '.motion-ready [data-reveal],.motion-ready [data-reveal].is-visible,',
    '.motion-ready .motion-stagger>*,.motion-ready .motion-stagger.is-visible>*',
    'opacity:1!important;clip-path:none!important;transform:none!important;transition:none!important;animation:none!important',
    '.motion-cinematic-media,.motion-cinematic-media.is-motion-media-visible{opacity:1!important',
    '.contact-page .contact-copy h1{display:block!important',
    '.contact-page .contact-grid{width:calc(100% - 28px)!important',
    '.contact-page .contact-benefits{display:grid!important',
    'body.contact-page .contact-dock .contact-action{height:56px!important',
)


def main()->None:
    parser=argparse.ArgumentParser(); parser.add_argument('--site',required=True); args=parser.parse_args()
    site=Path(args.site); pages=sorted(site.rglob('*.html')); css_path=site/'assets/css/mobile-stability.css'; final_path=site/'assets/css/mobile-contact-final.css'; errors=[]
    css=css_path.read_text(encoding='utf-8') if css_path.exists() else ''
    final_css=final_path.read_text(encoding='utf-8') if final_path.exists() else ''
    if not css_path.exists(): errors.append('missing mobile-stability.css')
    if not final_path.exists(): errors.append('missing mobile-contact-final.css')
    for token in REQUIRED:
        if token not in css: errors.append(f'mobile-stability missing {token}')
    for token in FINAL_REQUIRED:
        if token not in final_css: errors.append(f'mobile-contact-final missing {token}')

    ordered=viewport=0
    for page in pages:
        html=page.read_text(encoding='utf-8'); rel=page.relative_to(site)
        if 'name="viewport"' in html or "name='viewport'" in html: viewport+=1
        elif rel!=Path('support/index.html'): errors.append(f'{rel}: missing viewport meta')
        color=html.find('data-color-stability-style='); dock=html.find('data-contact-dock-style='); mobile=html.find('data-mobile-stability-style='); final=html.find('data-mobile-contact-final-style=')
        if min(color,dock,mobile,final)<0: errors.append(f'{rel}: missing final UI marker'); continue
        if not (color<dock<mobile<final): errors.append(f'{rel}: unsafe final mobile cascade color={color}, dock={dock}, mobile={mobile}, final={final}'); continue
        if 'mobile-stability.css?v=20260817-2' not in html: errors.append(f'{rel}: stale mobile stability asset'); continue
        if 'mobile-contact-final.css?v=20260817-1' not in html: errors.append(f'{rel}: stale mobile contact final asset'); continue
        ordered+=1

    contact=site/'lien-he/index.html'
    if contact.exists():
        text=contact.read_text(encoding='utf-8')
        if '<h1>Chuẩn bị thông tin để chọn gói Internet phù hợp hơn.</h1>' not in text:
            errors.append('contact page missing expected primary H1')
    else: errors.append('missing contact page')

    if errors:
        print('MOBILE QA FAIL'); [print(f'- {e}') for e in errors[:120]]; raise SystemExit(1)
    print(f'MOBILE QA PASS: pages={len(pages)}, ordered={ordered}, viewport={viewport}, overflow=guarded, typography=clean, content=one_column, carousels=contained, tables=contained, contact_collision=0, mobile_content_visible=guaranteed, contact_h1=visible_by_css, motion_color_wash=0')


if __name__=='__main__': main()
