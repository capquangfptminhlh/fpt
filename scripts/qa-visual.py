from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    pages = sorted(site.rglob('*.html'))
    errors: list[str] = []

    css = site / 'assets/css/apple-polish.css'
    contact_css = site / 'assets/css/apple-contact.css'
    dock_css = site / 'assets/css/contact-dock.css'
    text = css.read_text(encoding='utf-8') if css.exists() else ''
    contact_text = contact_css.read_text(encoding='utf-8') if contact_css.exists() else ''
    dock_text = dock_css.read_text(encoding='utf-8') if dock_css.exists() else ''
    if not css.exists(): errors.append('Missing assets/css/apple-polish.css')
    if not contact_css.exists(): errors.append('Missing assets/css/apple-contact.css')
    if not dock_css.exists(): errors.append('Missing assets/css/contact-dock.css')

    for token in (':root{','.topbar{','.home-v2 .m-hero h1{','.home-v2 .m-plan{','.subpage-hero{','.seo-hero{','.footer,.home-v2 .footer{','@media(max-width:760px)','@media(prefers-reduced-motion:reduce)','@keyframes apple-reveal'):
        if token not in text:
            errors.append(f'apple-polish.css missing rule: {token}')
    for token in ('.contact-hero{','.lead-card{','.contact-section{','.contact-callout{','@media(max-width:760px)'):
        if token not in contact_text:
            errors.append(f'apple-contact.css missing rule: {token}')

    for token in (
        'grid-template-columns:repeat(3,minmax(0,1fr))!important',
        'width:auto!important',
        'max-width:none!important',
        '.contact-copy small{display:none!important}',
        'white-space:nowrap!important',
        'overflow:hidden!important',
    ):
        if token not in dock_text:
            errors.append(f'contact-dock.css missing mobile overflow guard: {token}')

    for token in (
        '.contact-dock{--rail-bg:',
        'backdrop-filter:blur(22px)',
        '.contact-visual{',
        '.contact-orbit{',
        '.contact-copy{position:absolute;',
        '.contact-zalo{--accent:#0068ff',
        '.contact-call{--accent:#19a45a',
        '.contact-register{--accent:#f37021',
        '@keyframes contact-orbit',
        '@keyframes rail-glow-drift',
    ):
        if token not in dock_text:
            errors.append(f'contact-dock.css missing glass/motion treatment: {token}')

    forbidden_css = ('@import url(', 'fonts.googleapis.com', 'use.typekit.net')
    combined = (text + '\n' + contact_text + '\n' + dock_text).lower()
    for token in forbidden_css:
        if token in combined:
            errors.append(f'Visual CSS must not load external fonts: {token}')

    tagged = contact_tagged = dock_v11 = 0
    for page in pages:
        html = page.read_text(encoding='utf-8')
        rel = page.relative_to(site)
        polish_pos = html.find('data-apple-polish-style=')
        contact_pos = html.find('data-apple-contact-style=')
        transition_pos = html.find('data-page-transition-style=')
        if polish_pos < 0: errors.append(f'{rel}: missing Apple polish stylesheet')
        else: tagged += 1
        if contact_pos < 0: errors.append(f'{rel}: missing Apple contact stylesheet')
        else: contact_tagged += 1
        if 'contact-dock.css?v=20260817-11' not in html or 'contact-dock.js?v=20260817-10' not in html:
            errors.append(f'{rel}: missing contact dock color-safe assets')
        else:
            dock_v11 += 1
        if transition_pos >= 0 and polish_pos >= 0 and polish_pos < transition_pos:
            errors.append(f'{rel}: Apple polish must load after transition styles')
        if polish_pos >= 0 and contact_pos >= 0 and contact_pos < polish_pos:
            errors.append(f'{rel}: Apple contact polish must load after global Apple polish')

    if errors:
        print('VISUAL QA FAIL')
        for item in errors[:80]: print(f'- {item}')
        raise SystemExit(1)

    print(f'VISUAL QA PASS: pages={len(pages)}, apple_polish={tagged}, apple_contact={contact_tagged}, mobile_dock_v11={dock_v11}, glass_contact_rail=ready, external_fonts=0, responsive=ready')


if __name__ == '__main__':
    main()
