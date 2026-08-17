from __future__ import annotations

import argparse
from pathlib import Path

CSS_REQUIRED = (
    'overflow:visible!important',
    '.topbar .mobile-toggle[aria-expanded="true"]::before',
    '.topbar .mobile-toggle[aria-expanded="true"]::after',
    '.topbar .nav-links{',
    'opacity:0!important;visibility:hidden!important;pointer-events:none!important',
    '.topbar .nav-links.open{',
    'opacity:1!important;visibility:visible!important;pointer-events:auto!important',
    'body.nav-open .contact-dock{opacity:0!important;visibility:hidden!important;pointer-events:none!important}',
    '@media(prefers-reduced-motion:reduce)',
)
JS_REQUIRED = (
    "navLinks.classList.toggle('open')",
    "document.body.classList.toggle('nav-open', isOpen)",
    "toggle.setAttribute('aria-expanded', String(isOpen))",
    "event.key === 'Escape'",
    "!navLinks.contains(event.target) && !toggle.contains(event.target)",
    "if (!event.matches) closeMenu()",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    pages = sorted(site.rglob('*.html'))
    errors: list[str] = []

    css_path = site / 'assets/css/mobile-nav-final.css'
    js_path = site / 'assets/js/main.js'
    css = css_path.read_text(encoding='utf-8') if css_path.exists() else ''
    js = js_path.read_text(encoding='utf-8') if js_path.exists() else ''

    if not css_path.exists():
        errors.append('missing mobile-nav-final.css')
    for token in CSS_REQUIRED:
        if token not in css:
            errors.append(f'mobile-nav-final.css missing: {token}')
    if not js_path.exists():
        errors.append('missing main.js')
    for token in JS_REQUIRED:
        if token not in js:
            errors.append(f'main.js missing menu behavior: {token}')

    ordered = 0
    nav_pages = 0
    for page in pages:
        html = page.read_text(encoding='utf-8')
        rel = page.relative_to(site)
        nav_marker = html.find('data-mobile-nav-final-style=')
        mobile_marker = html.find('data-mobile-stability-style=')
        contact_marker = html.find('data-mobile-contact-final-style=')
        if nav_marker < 0:
            errors.append(f'{rel}: missing isolated mobile nav stylesheet')
            continue
        if not (mobile_marker >= 0 and contact_marker >= 0 and mobile_marker < contact_marker < nav_marker):
            errors.append(f'{rel}: unsafe nav cascade mobile={mobile_marker} contact={contact_marker} nav={nav_marker}')
            continue
        if 'mobile-nav-final.css?v=20260817-1' not in html:
            errors.append(f'{rel}: stale mobile nav asset')
            continue
        ordered += 1

        has_toggle = 'class="mobile-toggle"' in html
        has_nav = 'class="nav-links"' in html
        if has_toggle or has_nav:
            if not (has_toggle and has_nav):
                errors.append(f'{rel}: incomplete mobile menu markup')
            else:
                nav_pages += 1

    if nav_pages < 70:
        errors.append(f'expected menu markup on >=70 pages, found {nav_pages}')

    if errors:
        print('NAV QA FAIL')
        for error in errors[:100]:
            print(f'- {error}')
        raise SystemExit(1)

    print(
        f'NAV QA PASS: pages={len(pages)}, ordered={ordered}, nav_pages={nav_pages}, '
        'header_overflow=visible, closed=noninteractive, open=interactive, '
        'hamburger_state=aria_driven, dock_overlap=blocked, escape=ready, outside_click=ready'
    )


if __name__ == '__main__':
    main()
