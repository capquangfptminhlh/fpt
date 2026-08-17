from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_COLOR_TOKENS = (
    '--brand-bg:#f4f7fb;',
    '--brand-ink:#0b1324;',
    '--brand-blue:#0b72e7;',
    '--brand-orange:#f37021;',
    '.home-v2 .m-hero h1',
    '.seo-hero h1',
    '.lead-bar h1',
    '.contact-callout h1',
    '.footer h1',
    '.motion-cinematic-media,.motion-cinematic-media:hover{filter:none!important}',
    '.motion-fiber-canvas{mix-blend-mode:normal!important;',
    '@media(prefers-reduced-motion:reduce)',
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    pages = sorted(site.rglob('*.html'))
    errors: list[str] = []

    color_path = site / 'assets/css/color-stability.css'
    full_motion_path = site / 'assets/css/full-page-motion.css'
    apple_path = site / 'assets/css/apple-polish.css'
    dock_path = site / 'assets/css/contact-dock.css'

    for path in (color_path, full_motion_path, apple_path, dock_path):
        if not path.exists():
            errors.append(f'Missing {path.relative_to(site)}')

    color_css = color_path.read_text(encoding='utf-8') if color_path.exists() else ''
    full_css = full_motion_path.read_text(encoding='utf-8') if full_motion_path.exists() else ''
    apple_css = apple_path.read_text(encoding='utf-8') if apple_path.exists() else ''

    for token in REQUIRED_COLOR_TOKENS:
        if token not in color_css:
            errors.append(f'color-stability.css missing: {token}')

    if 'filter:saturate' in full_css or 'contrast(' in full_css or 'blur(' in full_css:
        errors.append('full-page motion still alters image color/blur')
    if '.contact-dock{gap:8px;width:170px}' not in apple_css:
        errors.append('expected legacy dock override signature changed; review cascade gate')

    ordered = 0
    for page in pages:
        html = page.read_text(encoding='utf-8')
        rel = page.relative_to(site)
        markers = [
            'data-apple-polish-style=',
            'data-motion-system-style=',
            'data-full-page-motion-style=',
            'data-color-stability-style=',
            'data-contact-dock-style=',
        ]
        positions = [html.find(marker) for marker in markers]
        if any(pos < 0 for pos in positions):
            errors.append(f'{rel}: missing one or more global theme styles')
            continue
        if positions != sorted(positions):
            errors.append(f'{rel}: unsafe stylesheet order {positions}')
            continue
        if 'color-stability.css?v=20260817-1' not in html:
            errors.append(f'{rel}: missing color stability v1')
            continue
        if 'contact-dock.css?v=20260817-11' not in html:
            errors.append(f'{rel}: contact dock not cache-busted/reordered')
            continue
        ordered += 1

    if errors:
        print('COLOR QA FAIL')
        for item in errors[:120]:
            print(f'- {item}')
        raise SystemExit(1)

    print(
        f'COLOR QA PASS: pages={len(pages)}, ordered={ordered}, canonical_tokens=ready, '
        'dark_contexts=ready, light_surfaces=ready, image_color_preservation=ready, '
        'contact_dock_last=ready, motion_tint_guard=ready'
    )


if __name__ == '__main__':
    main()
