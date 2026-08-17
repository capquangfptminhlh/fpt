from __future__ import annotations

import argparse
from pathlib import Path

STYLE = '<link rel="stylesheet" href="/fpt/assets/css/contact-dock.css?v=20260817-1" data-contact-dock-style="true"/>'
SCRIPT = '<script defer src="/fpt/assets/js/contact-dock.js?v=20260817-1" data-contact-dock-script="true"></script>'


def inject(html: str) -> str:
    if 'data-contact-dock-style=' not in html:
        if '</head>' not in html:
            raise ValueError('missing </head>')
        html = html.replace('</head>', f'{STYLE}</head>', 1)
    if 'data-contact-dock-script=' not in html:
        if '</body>' not in html:
            raise ValueError('missing </body>')
        html = html.replace('</body>', f'{SCRIPT}</body>', 1)
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

    print(f'Contact dock injected: {len(pages)} pages ({changed} changed)')


if __name__ == '__main__':
    main()
