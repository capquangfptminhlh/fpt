from __future__ import annotations

import argparse
from pathlib import Path

LEGACY_TOKENS = (
    'apple-polish.css', 'apple-contact.css', 'motion-system.css', 'full-page-motion.css',
    'color-stability.css', 'mobile-stability.css', 'mobile-contact-final.css',
    'mobile-nav-final.css', 'mobile-v3.css', 'motion-system.js', 'full-page-motion.js',
)
REQUIRED_UI = (
    '--ui-bg:#f6f7f9', '--ui-ink:#111827', '--ui-orange:#f37021',
    '.topbar,.home-v2 .topbar{', '.nav-links.open{', '.contact-dock{',
    '.contact-page .contact-copy h1{', '@media(max-width:760px)',
    'body.nav-open .contact-dock', 'overflow-x:hidden',
)
REQUIRED_MOTION = (
    '.ui-reveal{transform:none;opacity:1}', '.ui-motion-ready .ui-reveal',
    '@media(prefers-reduced-motion:reduce)',
)
REQUIRED_MOTION_JS = (
    "body.classList.add('ui-motion-ready')", 'IntersectionObserver', 'showAll',
    "body.classList.toggle('ui-scrolled'", 'prefers-reduced-motion: reduce',
)


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--site',required=True); args=parser.parse_args()
    site=Path(args.site); pages=sorted(site.rglob('*.html')); errors=[]
    ui=site/'assets/css/ui-reset.css'; motion=site/'assets/css/ui-motion.css'; motion_js=site/'assets/js/ui-motion.js'; main_js=site/'assets/js/main.js'
    ui_text=ui.read_text(encoding='utf-8') if ui.exists() else ''
    motion_text=motion.read_text(encoding='utf-8') if motion.exists() else ''
    motion_js_text=motion_js.read_text(encoding='utf-8') if motion_js.exists() else ''
    main_js_text=main_js.read_text(encoding='utf-8') if main_js.exists() else ''

    if not ui.exists(): errors.append('missing ui-reset.css')
    if not motion.exists(): errors.append('missing ui-motion.css')
    if not motion_js.exists(): errors.append('missing ui-motion.js')
    for token in REQUIRED_UI:
        if token not in ui_text: errors.append(f'ui-reset missing {token}')
    for token in REQUIRED_MOTION:
        if token not in motion_text: errors.append(f'ui-motion missing {token}')
    for token in REQUIRED_MOTION_JS:
        if token not in motion_js_text: errors.append(f'ui-motion.js missing {token}')
    if 'opacity:0' in motion_text.replace('opacity:0;', ''):
        errors.append('ui-motion contains unsafe opacity hiding')
    if 'mix-blend-mode' in ui_text or 'mix-blend-mode' in motion_text:
        errors.append('reset UI must not use mix-blend-mode')
    if 'mobile-v3.css' in main_js_text or 'data-mobile-v3' in main_js_text:
        errors.append('main.js still injects mobile-v3')
    if 'mobile-bottom-cta' in main_js_text:
        errors.append('main.js still creates legacy bottom CTA')

    ordered=0
    for page in pages:
        text=page.read_text(encoding='utf-8'); rel=page.relative_to(site)
        reset=text.find('data-ui-reset-style='); motion_pos=text.find('data-ui-motion-style='); transition=text.find('data-page-transition-style=')
        if min(reset,motion_pos,transition)<0:
            errors.append(f'{rel}: missing reset/motion/transition marker'); continue
        if not (transition < reset < motion_pos): errors.append(f'{rel}: unsafe stylesheet order')
        for token in LEGACY_TOKENS:
            if token in text: errors.append(f'{rel}: legacy runtime asset loaded: {token}')
        if 'data-contact-dock-script=' not in text: errors.append(f'{rel}: missing contact dock script')
        ordered += 1

    contact=site/'lien-he/index.html'
    if contact.exists():
        text=contact.read_text(encoding='utf-8')
        if 'data-ui-reset-style=' not in text: errors.append('contact page missing reset style')
    else: errors.append('contact page missing')

    if errors:
        print('UI RESET QA FAIL'); [print(f'- {e}') for e in errors[:120]]; raise SystemExit(1)
    print(f'UI RESET QA PASS: pages={len(pages)}, ordered={ordered}, legacy_runtime_layers=0, mobile_content_visible=default, nav=isolated, dock=contained, motion=progressive')


if __name__=='__main__': main()
