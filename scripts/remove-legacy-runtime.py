from __future__ import annotations

import argparse
import re
from pathlib import Path

LEGACY_ASSETS = (
    'apple-polish.css',
    'apple-contact.css',
    'motion-system.css',
    'full-page-motion.css',
    'color-stability.css',
    'mobile-stability.css',
    'mobile-contact-final.css',
    'mobile-nav-final.css',
    'mobile-v3.css',
    'motion-system.js',
    'full-page-motion.js',
)

ASSET_ALT = '|'.join(re.escape(item) for item in LEGACY_ASSETS)
LINK_RE = re.compile(
    rf'<link\b[^>]*href=["\'][^"\']*(?:{ASSET_ALT})[^"\']*["\'][^>]*?/?>',
    flags=re.I | re.S,
)
SCRIPT_RE = re.compile(
    rf'<script\b[^>]*src=["\'][^"\']*(?:{ASSET_ALT})[^"\']*["\'][^>]*>.*?</script>',
    flags=re.I | re.S,
)


def clean_html(text: str) -> tuple[str, int]:
    text, scripts = SCRIPT_RE.subn('', text)
    text, links = LINK_RE.subn('', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text, scripts + links


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)

    if not site.exists():
        raise SystemExit(f'LEGACY RUNTIME CLEAN FAIL: missing site {site}')

    pages = sorted(site.rglob('*.html'))
    removed = 0
    changed = 0
    errors: list[str] = []

    for page in pages:
        original = page.read_text(encoding='utf-8')
        updated, count = clean_html(original)
        if count:
            page.write_text(updated, encoding='utf-8')
            removed += count
            changed += 1

    for page in pages:
        text = page.read_text(encoding='utf-8')
        for token in LEGACY_ASSETS:
            if token in text:
                errors.append(f'{page.relative_to(site)} still loads {token}')

    main_js = site / 'assets/js/main.js'
    if main_js.exists():
        main_text = main_js.read_text(encoding='utf-8')
        if 'mobile-v3.css' in main_text or 'data-mobile-v3' in main_text:
            errors.append('assets/js/main.js still injects mobile-v3 runtime')
        if 'mobile-bottom-cta' in main_text:
            errors.append('assets/js/main.js still creates legacy mobile bottom CTA')

    if errors:
        print('LEGACY RUNTIME CLEAN FAIL')
        for error in errors[:100]:
            print(f'- {error}')
        raise SystemExit(1)

    print(
        f'LEGACY RUNTIME CLEAN PASS: pages={len(pages)}, '
        f'changed={changed}, tags_removed={removed}, legacy_runtime_layers=0'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
