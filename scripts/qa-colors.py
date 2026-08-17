from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--site',required=True); args=parser.parse_args()
    site=Path(args.site); pages=sorted(site.rglob('*.html')); errors=[]
    color=(site/'assets/css/color-stability.css').read_text(encoding='utf-8')
    motion=(site/'assets/css/full-page-motion.css').read_text(encoding='utf-8')
    mobile=(site/'assets/css/mobile-stability.css').read_text(encoding='utf-8')
    for token in ('--brand-bg:#f4f7fb;','--brand-ink:#0b1324;','--brand-blue:#0b72e7;','--brand-orange:#f37021;','.motion-cinematic-media,.motion-cinematic-media:hover{filter:none!important}'):
        if token not in color: errors.append(f'color-stability missing {token}')
    if 'filter:saturate' in motion or 'contrast(' in motion or 'blur(' in motion: errors.append('full-page motion recolors or blurs media')
    for token in ('.motion-section::before,.motion-section::after,.motion-section-beam,.motion-footer-field,.motion-fiber-canvas,.motion-glow::before{display:none!important}','background:#f4f7fb!important;color:#0b1324!important'):
        if token not in mobile: errors.append(f'mobile final palette missing {token}')
    ordered=0
    for page in pages:
        html=page.read_text(encoding='utf-8'); rel=page.relative_to(site)
        markers=['data-apple-polish-style=','data-motion-system-style=','data-full-page-motion-style=','data-color-stability-style=','data-contact-dock-style=','data-mobile-stability-style=']
        pos=[html.find(x) for x in markers]
        if any(x<0 for x in pos): errors.append(f'{rel}: missing theme styles'); continue
        if pos!=sorted(pos): errors.append(f'{rel}: unsafe final cascade {pos}'); continue
        if 'color-stability.css?v=20260817-1' not in html or 'contact-dock.css?v=20260817-12' not in html or 'mobile-stability.css?v=20260817-2' not in html: errors.append(f'{rel}: stale theme asset version'); continue
        ordered+=1
    if errors:
        print('COLOR QA FAIL'); [print(f'- {e}') for e in errors[:120]]; raise SystemExit(1)
    print(f'COLOR QA PASS: pages={len(pages)}, ordered={ordered}, palette=stable, media_color=preserved, mobile_ambient=disabled')


if __name__=='__main__': main()
