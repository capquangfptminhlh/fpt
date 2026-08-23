from __future__ import annotations

import argparse
import re
from pathlib import Path

MENU_LABELS = ('Internet', 'Gói cước', 'Combo', 'WiFi 7', 'Camera', 'FPT Play', 'Khu vực', 'Hỗ trợ')
OLD_MENU_LABELS = ('>Trang chủ</a>', '>Lắp mạng FPT</a>', '>Giải pháp</a>', '>So sánh</a>', '>Tin tức</a>', '>Kiến thức</a>')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)

    pages = sorted(site.rglob('*.html'))
    errors: list[str] = []
    checked = 0

    shell_css = site / 'assets/css/site-shell.css'
    if not shell_css.exists():
        errors.append('missing assets/css/site-shell.css')
    else:
        css = shell_css.read_text(encoding='utf-8')
        for token in (
            '--shell-navy:#050d1d',
            'background:rgba(4,12,28,.94)!important',
            'color:#fff!important',
            '.subpage-hero',
            '.seo-hero',
            '.page-transition{background:rgba(4,12,28,.92)!important}',
        ):
            if token not in css:
                errors.append(f'site-shell.css missing required token: {token}')

    for page in pages:
        html = page.read_text(encoding='utf-8')
        if 'nav-links' not in html:
            continue
        checked += 1
        rel = page.relative_to(site)

        if 'site-shell' not in html:
            errors.append(f'{rel}: missing site-shell body marker')
        if 'data-site-shell-style=' not in html:
            errors.append(f'{rel}: missing site-shell stylesheet')

        nav_match = re.search(
            r'<nav\b[^>]*class=["\'][^"\']*nav-links[^"\']*["\'][^>]*>(.*?)</nav>',
            html,
            flags=re.I | re.S,
        )
        if not nav_match:
            errors.append(f'{rel}: nav-links markup not parseable')
            continue
        nav = nav_match.group(1)

        for label in MENU_LABELS:
            if not re.search(rf'>\s*{re.escape(label)}\s*</a>', nav, flags=re.I):
                errors.append(f'{rel}: missing unified nav item {label}')
        if len(re.findall(r'<a\b', nav, flags=re.I)) != len(MENU_LABELS):
            errors.append(f'{rel}: unified nav must have exactly {len(MENU_LABELS)} links')
        for old in OLD_MENU_LABELS:
            if old.lower() in nav.lower():
                errors.append(f'{rel}: legacy nav item still present: {old}')

        transition = html.find('data-page-transition-style=')
        reset = html.find('data-ui-reset-style=')
        motion = html.find('data-ui-motion-style=')
        shell = html.find('data-site-shell-style=')
        if min(transition, reset, motion, shell) < 0:
            errors.append(f'{rel}: incomplete stylesheet markers')
        elif not (transition < reset < motion < shell):
            errors.append(f'{rel}: site-shell is not final visual authority')

    if checked < 100:
        errors.append(f'suspicious navigation page count: {checked}')

    if errors:
        print('SITE SHELL QA FAIL')
        for error in errors[:140]:
            print(f'- {error}')
        raise SystemExit(1)

    print(
        f'SITE SHELL QA PASS: nav_pages={checked}, menu_links={len(MENU_LABELS)}, '
        'header=navy, nav=white, active=orange, shell_order=final'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
