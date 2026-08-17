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
    if not css.exists():
        errors.append('Missing assets/css/apple-polish.css')
        text = ''
    else:
        text = css.read_text(encoding='utf-8')

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

    forbidden_css = ('@import url(', 'fonts.googleapis.com', 'use.typekit.net')
    for token in forbidden_css:
        if token in text.lower():
            errors.append(f'apple-polish.css must not load external fonts: {token}')

    tagged = 0
    for page in pages:
        html = page.read_text(encoding='utf-8')
        rel = page.relative_to(site)
        if 'data-apple-polish-style=' not in html:
            errors.append(f'{rel}: missing Apple polish stylesheet')
        else:
            tagged += 1
        if html.find('data-apple-polish-style=') < html.find('data-page-transition-style='):
            errors.append(f'{rel}: Apple polish must load after transition/contact styles')

    if errors:
        print('VISUAL QA FAIL')
        for item in errors[:80]:
            print(f'- {item}')
        raise SystemExit(1)

    print(f'VISUAL QA PASS: pages={len(pages)}, apple_polish={tagged}, external_fonts=0, responsive=ready')


if __name__ == '__main__':
    main()
