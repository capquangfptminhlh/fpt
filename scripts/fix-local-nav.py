from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    changed = 0
    checked = 0

    pattern = re.compile(r'(<nav\b[^>]*class=["\'][^"\']*nav-links[^"\']*["\'][^>]*>)(.*?)(</nav>)', re.I | re.S)
    for path in site.rglob('*.html'):
        html = path.read_text(encoding='utf-8')
        match = pattern.search(html)
        if not match:
            continue
        checked += 1
        nav_inner = match.group(2)
        if re.search(r'>\s*Khu vực\s*</a>', nav_inner, flags=re.I):
            continue
        rel = Path(os.path.relpath(site / 'khu-vuc', path.parent)).as_posix()
        href = (rel.rstrip('/') + '/') if rel != '.' else './'
        replacement = match.group(1) + nav_inner + f'<a href="{href}">Khu vực</a>' + match.group(3)
        html = html[:match.start()] + replacement + html[match.end():]
        path.write_text(html, encoding='utf-8')
        changed += 1

    print(f'Khu vực nav fixed: checked={checked}, changed={changed}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
