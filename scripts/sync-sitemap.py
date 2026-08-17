from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree, register_namespace


def url_for(relative: Path, origin: str) -> str:
    parts = relative.parts
    if parts[-1] == 'index.html':
        path = '/'.join(parts[:-1])
        return f'{origin}/{path}/' if path else f'{origin}/'
    return f'{origin}/' + '/'.join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    parser.add_argument('--origin', required=True)
    parser.add_argument('--lastmod', default=date.today().isoformat())
    args = parser.parse_args()
    site = Path(args.site)
    origin = args.origin.rstrip('/')

    urls = sorted({url_for(p.relative_to(site), origin) for p in site.rglob('*.html')})
    register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    root = Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
    for url in urls:
        node = SubElement(root, '{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        SubElement(node, '{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text = url
        SubElement(node, '{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod').text = args.lastmod
    ElementTree(root).write(site / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    print(f'Sitemap synced: {len(urls)} HTML URLs')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
