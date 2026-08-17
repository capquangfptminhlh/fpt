from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_CSS = (
    '.motion-progress{',
    '.motion-ready [data-reveal]{',
    '.motion-ready .motion-stagger>*{',
    '.motion-glow::before{',
    '.motion-magnetic{',
    '.motion-tilt{',
    '@keyframes aurora-drift',
    '@keyframes price-pop',
    '@media(max-width:760px)',
    '@media(prefers-reduced-motion:reduce)',
)
REQUIRED_JS = (
    "prefers-reduced-motion: reduce",
    'IntersectionObserver',
    'requestAnimationFrame(updateScroll)',
    "motion-progress",
    "motion-stagger",
    "motion-glow",
    "motion-tilt",
    "motion-magnetic",
    "pageshow",
    "FPTMotionSystem",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    pages = sorted(site.rglob('*.html'))
    errors: list[str] = []

    css_path = site / 'assets/css/motion-system.css'
    js_path = site / 'assets/js/motion-system.js'
    css = css_path.read_text(encoding='utf-8') if css_path.exists() else ''
    js = js_path.read_text(encoding='utf-8') if js_path.exists() else ''

    if not css_path.exists():
        errors.append('Missing assets/css/motion-system.css')
    if not js_path.exists():
        errors.append('Missing assets/js/motion-system.js')

    for token in REQUIRED_CSS:
        if token not in css:
            errors.append(f'motion-system.css missing: {token}')
    for token in REQUIRED_JS:
        if token not in js:
            errors.append(f'motion-system.js missing: {token}')

    if '.motion-glow>*{position:' in css:
        errors.append('motion glow must not override child positioning')
    if 'setInterval(' in js:
        errors.append('motion system must not use continuous setInterval loops')
    if 'requestAnimationFrame(updateScroll)' not in js:
        errors.append('scroll motion must be requestAnimationFrame throttled')

    styled = scripted = 0
    for page in pages:
        html = page.read_text(encoding='utf-8')
        rel = page.relative_to(site)
        if 'motion-system.css?v=20260817-8' not in html or 'data-motion-system-style=' not in html:
            errors.append(f'{rel}: missing motion v8 stylesheet')
        else:
            styled += 1
        if 'motion-system.js?v=20260817-8' not in html or 'data-motion-system-script=' not in html:
            errors.append(f'{rel}: missing motion v8 script')
        else:
            scripted += 1

    if errors:
        print('MOTION QA FAIL')
        for item in errors[:80]:
            print(f'- {item}')
        raise SystemExit(1)

    print(
        f'MOTION QA PASS: pages={len(pages)}, styled={styled}, scripted={scripted}, '
        'reveal=ready, stagger=ready, parallax=ready, glow=ready, tilt=ready, '
        'magnetic=ready, progress=ready, reduced_motion=ready'
    )


if __name__ == '__main__':
    main()
