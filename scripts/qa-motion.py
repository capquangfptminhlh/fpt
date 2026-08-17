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
    '.motion-fiber-canvas{',
    '.motion-signal-field{',
    '.home-v2 .m-plan.is-auto-focus{',
    '@keyframes signal-wave',
    '@keyframes cta-sheen',
    '@keyframes aurora-drift',
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
    "motion-fiber-canvas",
    "motion-signal-field",
    "is-auto-focus",
    "navigator.hardwareConcurrency",
    "connection?.saveData",
    "document.hidden",
    "visibilitychange",
    "version: '10'",
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
    if not css_path.exists(): errors.append('Missing assets/css/motion-system.css')
    if not js_path.exists(): errors.append('Missing assets/js/motion-system.js')

    for token in REQUIRED_CSS:
        if token not in css: errors.append(f'motion-system.css missing: {token}')
    for token in REQUIRED_JS:
        if token not in js: errors.append(f'motion-system.js missing: {token}')

    if '.motion-glow>*{position:' in css:
        errors.append('motion glow must not override child positioning')
    if 'setInterval(' in js:
        errors.append('motion system must not use continuous setInterval loops')
    if 'cancelAnimationFrame' not in js:
        errors.append('fiber animation must stop its RAF when inactive')
    if 'clearTimeout(planFocusTimer)' not in js:
        errors.append('automated plan focus must be stoppable')

    styled = scripted = 0
    for page in pages:
        html = page.read_text(encoding='utf-8')
        rel = page.relative_to(site)
        if 'motion-system.css?v=20260817-10' not in html or 'data-motion-system-style=' not in html:
            errors.append(f'{rel}: missing motion v10 stylesheet')
        else:
            styled += 1
        if 'motion-system.js?v=20260817-10' not in html or 'data-motion-system-script=' not in html:
            errors.append(f'{rel}: missing motion v10 script')
        else:
            scripted += 1

    if errors:
        print('MOTION QA FAIL')
        for item in errors[:80]: print(f'- {item}')
        raise SystemExit(1)

    print(
        f'MOTION QA PASS: pages={len(pages)}, styled={styled}, scripted={scripted}, '
        'reveal=ready, stagger=ready, fiber_canvas=ready, signal_waves=ready, '
        'auto_focus=ready, glow=ready, tilt=ready, magnetic=ready, progress=ready, '
        'visibility_pause=ready, low_power_guard=ready, reduced_motion=ready'
    )


if __name__ == '__main__':
    main()
