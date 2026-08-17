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
    if not css.exists():
        errors.append('Missing assets/css/apple-polish.css')
        text = ''
    else:
        text = css.read_text(encoding='utf-8')
    if not contact_css.exists():
        errors.append('Missing assets/css/apple-contact.css')
        contact_text = ''
    else:
        contact_text = contact_css.read_text(encoding='utf-8')

    required_css = (
        ':root{',
        '.topbar{',
        '.home-v2 .m-hero h1{',
        '.home-v2 .m-plan{',
        '.subpage-hero{',
        '.seo-hero{',
        '.footer,.home-v2 .footer{',
        '@media(max-width:760px)',
        '@media(prefers-reduced-motion:reduce)',
        '@keyframes apple-reveal',
    )
    for token in required_css:
        if token not in text:
            errors.append(f'apple-polish.css missing rule: {token}')

    for token in ('.contact-hero{', '.lead-card{', '.contact-section{', '.contact-callout{', '@media(max-width:760px)'):
        if token not in contact_text:
            errors.append(f'apple-contact.css missing rule: {token}')

    forbidden_css = ('@import url(', 'fonts.googleapis.com', 'use.typekit.net')
    combined = (text + '\n' + contact_text).lower()
    for token in forbidden_css:
        if token in combined:
            errors.append(f'Apple visual CSS must not load external fonts: {token}')

    tagged = 0
    contact_tagged = 0
    for page in pages:
        html = page.read_text(encoding='utf-8')
        rel = page.relative_to(site)
        polish_pos = html.find('data-apple-polish-style=')
        contact_pos = html.find('data-apple-contact-style=')
        transition_pos = html.find('data-page-transition-style=')
        if polish_pos < 0:
            errors.append(f'{rel}: missing Apple polish stylesheet')
        else:
            tagged += 1
        if contact_pos < 0:
            errors.append(f'{rel}: missing Apple contact stylesheet')
        else:
            contact_tagged += 1
        if transition_pos >= 0 and polish_pos >= 0 and polish_pos < transition_pos:
            errors.append(f'{rel}: Apple polish must load after transition/contact styles')
        if polish_pos >= 0 and contact_pos >= 0 and contact_pos < polish_pos:
            errors.append(f'{rel}: Apple contact polish must load after global Apple polish')

    if errors:
        print('VISUAL QA FAIL')
        for item in errors[:80]:
            print(f'- {item}')
        raise SystemExit(1)

    print(
        f'VISUAL QA PASS: pages={len(pages)}, apple_polish={tagged}, '
        f'apple_contact={contact_tagged}, external_fonts=0, responsive=ready'
    )


if __name__ == '__main__':
    main()
