from __future__ import annotations

import argparse
from pathlib import Path

CONTACT_STYLE = '<link rel="stylesheet" href="/fpt/assets/css/contact-dock.css?v=20260817-4" data-contact-dock-style="true"/>'
CONTACT_SCRIPT = '<script defer src="/fpt/assets/js/contact-dock.js?v=20260817-3" data-contact-dock-script="true"></script>'
TRANSITION_STYLE = '<link rel="stylesheet" href="/fpt/assets/css/page-transition.css?v=20260817-1" data-page-transition-style="true"/>'
TRANSITION_SCRIPT = '<script defer src="/fpt/assets/js/page-transition.js?v=20260817-2" data-page-transition-script="true"></script>'
APPLE_STYLE = '<link rel="stylesheet" href="/fpt/assets/css/apple-polish.css?v=20260817-2" data-apple-polish-style="true"/>'
APPLE_CONTACT_STYLE = '<link rel="stylesheet" href="/fpt/assets/css/apple-contact.css?v=20260817-1" data-apple-contact-style="true"/>'
MOTION_STYLE = '<link rel="stylesheet" href="/fpt/assets/css/motion-system.css?v=20260817-8" data-motion-system-style="true"/>'
MOTION_SCRIPT = '<script defer src="/fpt/assets/js/motion-system.js?v=20260817-8" data-motion-system-script="true"></script>'


def inject(html: str) -> str:
    if '</head>' not in html:
        raise ValueError('missing </head>')
    if '</body>' not in html:
        raise ValueError('missing </body>')

    head_assets: list[str] = []
    if 'data-contact-dock-style=' not in html:
        head_assets.append(CONTACT_STYLE)
    if 'data-page-transition-style=' not in html:
        head_assets.append(TRANSITION_STYLE)
    if 'data-apple-polish-style=' not in html:
        head_assets.append(APPLE_STYLE)
    if 'data-apple-contact-style=' not in html:
        head_assets.append(APPLE_CONTACT_STYLE)
    if 'data-motion-system-style=' not in html:
        head_assets.append(MOTION_STYLE)
    if head_assets:
        html = html.replace('</head>', ''.join(head_assets) + '</head>', 1)

    body_assets: list[str] = []
    if 'data-contact-dock-script=' not in html:
        body_assets.append(CONTACT_SCRIPT)
    if 'data-page-transition-script=' not in html:
        body_assets.append(TRANSITION_SCRIPT)
    if 'data-motion-system-script=' not in html:
        body_assets.append(MOTION_SCRIPT)
    if body_assets:
        html = html.replace('</body>', ''.join(body_assets) + '</body>', 1)
    return html


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    pages = sorted(site.rglob('*.html'))
    if not pages:
        raise SystemExit('No HTML pages found')

    changed = 0
    for page in pages:
        old = page.read_text(encoding='utf-8')
        try:
            new = inject(old)
        except ValueError as exc:
            raise SystemExit(f'{page}: {exc}') from exc
        if new != old:
            page.write_text(new, encoding='utf-8')
            changed += 1

    print(f'Global UI assets injected: {len(pages)} pages ({changed} changed)')


if __name__ == '__main__':
    main()
