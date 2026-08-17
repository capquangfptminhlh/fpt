from __future__ import annotations

import argparse
import ast
import hashlib
import re
from html import unescape
from pathlib import Path

MIN_WORDS = 1250
MIN_HEADINGS = 13
MIN_FAQ = 9


def load_locations(path: Path) -> list[dict]:
    tree = ast.parse(path.read_text(encoding='utf-8'))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'LOCATIONS' for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit('LOCAL EDITORIAL QA FAIL: LOCATIONS not found')


def clean(html: str) -> str:
    text = re.sub(r'<script\b.*?</script>|<style\b.*?</style>', ' ', html, flags=re.I | re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    return re.sub(r'\s+', ' ', unescape(text)).strip()


def block(html: str, slug: str) -> str:
    match = re.search(r'<section class="local-editorial-v2"[^>]*>.*?</section>', html, flags=re.I | re.S)
    if not match:
        raise SystemExit(f'LOCAL EDITORIAL QA FAIL: {slug} editorial block missing')
    return match.group(0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    parser.add_argument('--locations-script', default='scripts/generate-local-pages.py')
    args = parser.parse_args()
    locations = load_locations(Path(args.locations_script))
    if len(locations) != 34:
        raise SystemExit(f'LOCAL EDITORIAL QA FAIL: expected 34 locations, got {len(locations)}')
    css = Path(args.site) / 'assets/css/local-editorial-v2.css'
    if not css.exists() or css.stat().st_size < 5000:
        raise SystemExit('LOCAL EDITORIAL QA FAIL: editorial CSS missing or too small')

    fingerprints: dict[str, str] = {}
    word_counts: list[int] = []
    for loc in locations:
        slug, name = loc['slug'], loc['name']
        path = Path(args.site) / 'khu-vuc' / slug / 'index.html'
        if not path.exists():
            raise SystemExit(f'LOCAL EDITORIAL QA FAIL: missing {slug}')
        html = path.read_text(encoding='utf-8')
        article = block(html, slug)
        if 'data-local-editorial-v2="true"' not in article or f'data-local-focus="{slug}"' not in article:
            raise SystemExit(f'LOCAL EDITORIAL QA FAIL: {slug} markers missing')
        if 'data-local-editorial-v2-style="true"' not in html:
            raise SystemExit(f'LOCAL EDITORIAL QA FAIL: {slug} CSS not injected')
        visible = clean(article)
        words = re.findall(r'\b[\wÀ-ỹ]+\b', visible, flags=re.UNICODE)
        if len(words) < MIN_WORDS:
            raise SystemExit(f'LOCAL EDITORIAL QA FAIL: {slug} too thin: {len(words)} words < {MIN_WORDS}')
        heading_count = len(re.findall(r'<h[23]\b', article, flags=re.I))
        if heading_count < MIN_HEADINGS:
            raise SystemExit(f'LOCAL EDITORIAL QA FAIL: {slug} headings={heading_count} < {MIN_HEADINGS}')
        if article.count('<details>') < MIN_FAQ:
            raise SystemExit(f'LOCAL EDITORIAL QA FAIL: {slug} FAQ < {MIN_FAQ}')
        for marker in ('editorial-table-wrap','editorial-checklist','editorial-steps','editorial-cards','#goi-dich-vu-dia-phuong'):
            if marker not in article:
                raise SystemExit(f'LOCAL EDITORIAL QA FAIL: {slug} missing {marker}')
        if visible.count(name) < 6:
            raise SystemExit(f'LOCAL EDITORIAL QA FAIL: {slug} local name too weak')
        merged = loc.get('merged_from') or []
        if len(merged) > 1:
            for old in merged:
                if old not in visible:
                    raise SystemExit(f'LOCAL EDITORIAL QA FAIL: {slug} predecessor {old} missing')
        lowered = visible.lower()
        forbidden = ('phủ sóng toàn tỉnh', 'hạ tầng phủ 100%', 'chắc chắn lắp được', 'cam kết lắp được mọi địa chỉ')
        if any(x in lowered for x in forbidden):
            raise SystemExit(f'LOCAL EDITORIAL QA FAIL: {slug} unsupported coverage claim')
        normalized = lowered
        for token in [name, *(merged or [])]:
            normalized = normalized.replace(token.lower(), '<loc>')
        normalized = re.sub(r'\s+', ' ', normalized)
        fp = hashlib.sha256(normalized.encode('utf-8')).hexdigest()
        if fp in fingerprints:
            raise SystemExit(f'LOCAL EDITORIAL QA FAIL: normalized duplicate {slug} == {fingerprints[fp]}')
        fingerprints[fp] = slug
        word_counts.append(len(words))

    print(f'LOCAL EDITORIAL QA PASS: 34/34 longform guides; min_words={min(word_counts)}, avg_words={sum(word_counts)//len(word_counts)}, headings>={MIN_HEADINGS}, FAQ={MIN_FAQ}, normalized fingerprints=34 unique; unsupported coverage claims=0')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
