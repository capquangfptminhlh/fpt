from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path
from xml.etree.ElementTree import Element, ElementTree, SubElement, register_namespace

NOINDEX_META = re.compile(
    r'<meta\b(?=[^>]*\bname=["\']robots["\'])(?=[^>]*\bcontent=["\'][^"\']*\bnoindex\b)[^>]*>',
    flags=re.I,
)


def url_for(relative: Path, origin: str) -> str:
    parts = relative.parts
    if parts[-1] == 'index.html':
        path = '/'.join(parts[:-1])
        return f'{origin}/{path}/' if path else f'{origin}/'
    return f'{origin}/' + '/'.join(parts)


def is_indexable_html(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    return NOINDEX_META.search(text) is None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    parser.add_argument('--origin', required=True)
    parser.add_argument('--lastmod', default=date.today().isoformat())
    args = parser.parse_args()
    site = Path(args.site)
    origin = args.origin.rstrip('/')

    html_files = sorted(site.rglob('*.html'))
    indexable = [path for path in html_files if is_indexable_html(path)]
    excluded = len(html_files) - len(indexable)
    urls = sorted({url_for(path.relative_to(site), origin) for path in indexable})

    register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    root = Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
    for url in urls:
        node = SubElement(root, '{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        SubElement(node, '{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text = url
        SubElement(node, '{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod').text = args.lastmod
    ElementTree(root).write(site / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    print(f'Sitemap synced: {len(urls)} indexable HTML URLs; noindex excluded={excluded}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
