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
FULL_REQUIRED_CSS = (
    '.motion-section{',
    '.motion-heading{',
    '.motion-cinematic-media{',
    '.motion-nav-link{',
    '.motion-ripple{',
    '.motion-section-beam{',
    '.motion-footer-field{',
    '--section-blue-alpha:',
    '--section-line-scale:',
    '@keyframes full-ripple',
    '@keyframes section-beam',
    '@keyframes footer-float',
    '@media(max-width:760px)',
    '@media(prefers-reduced-motion:reduce)',
)
FULL_REQUIRED_JS = (
    "prefers-reduced-motion: reduce",
    'IntersectionObserver',
    'requestAnimationFrame(updateFullPageScroll)',
    "motion-section",
    "motion-heading",
    "motion-cinematic-media",
    "motion-nav-link",
    "motion-ripple-host",
    "motion-section-beam",
    "motion-footer-field",
    "applySectionMotion",
    "--section-blue-alpha",
    "--section-line-scale",
    "navigator.hardwareConcurrency",
    "connection?.saveData",
    "document.hidden",
    "visibilitychange",
    "version: '11'",
    "FPTFullPageMotion",
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
    full_css_path = site / 'assets/css/full-page-motion.css'
    full_js_path = site / 'assets/js/full-page-motion.js'
    css = css_path.read_text(encoding='utf-8') if css_path.exists() else ''
    js = js_path.read_text(encoding='utf-8') if js_path.exists() else ''
    full_css = full_css_path.read_text(encoding='utf-8') if full_css_path.exists() else ''
    full_js = full_js_path.read_text(encoding='utf-8') if full_js_path.exists() else ''

    if not css_path.exists(): errors.append('Missing assets/css/motion-system.css')
    if not js_path.exists(): errors.append('Missing assets/js/motion-system.js')
    if not full_css_path.exists(): errors.append('Missing assets/css/full-page-motion.css')
    if not full_js_path.exists(): errors.append('Missing assets/js/full-page-motion.js')

    for token in REQUIRED_CSS:
        if token not in css: errors.append(f'motion-system.css missing: {token}')
    for token in REQUIRED_JS:
        if token not in js: errors.append(f'motion-system.js missing: {token}')
    for token in FULL_REQUIRED_CSS:
        if token not in full_css: errors.append(f'full-page-motion.css missing: {token}')
    for token in FULL_REQUIRED_JS:
        if token not in full_js: errors.append(f'full-page-motion.js missing: {token}')

    if '.motion-glow>*{position:' in css:
        errors.append('motion glow must not override child positioning')
    if 'setInterval(' in js or 'setInterval(' in full_js:
        errors.append('motion system must not use continuous setInterval loops')
    if 'cancelAnimationFrame' not in js:
        errors.append('fiber animation must stop its RAF when inactive')
    if 'clearTimeout(planFocusTimer)' not in js:
        errors.append('automated plan focus must be stoppable')
    if 'requestAnimationFrame(updateFullPageScroll)' not in full_js:
        errors.append('full-page scroll effects must be RAF throttled')
    if 'pointermove' in full_js and 'requestAnimationFrame' not in full_js:
        errors.append('full-page pointer effects must be RAF throttled')
    if '*.' in full_css or ')*' in full_css:
        errors.append('full-page CSS must avoid unsupported calc multiplication syntax')

    styled = scripted = full_styled = full_scripted = 0
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
        if 'full-page-motion.css?v=20260817-11a' not in html or 'data-full-page-motion-style=' not in html:
            errors.append(f'{rel}: missing full-page motion v11a stylesheet')
        else:
            full_styled += 1
        if 'full-page-motion.js?v=20260817-11a' not in html or 'data-full-page-motion-script=' not in html:
            errors.append(f'{rel}: missing full-page motion v11a script')
        else:
            full_scripted += 1

    if errors:
        print('MOTION QA FAIL')
        for item in errors[:100]: print(f'- {item}')
        raise SystemExit(1)

    print(
        f'MOTION QA PASS: pages={len(pages)}, base_styled={styled}, base_scripted={scripted}, '
        f'full_styled={full_styled}, full_scripted={full_scripted}, reveal=ready, stagger=ready, '
        'fiber_canvas=ready, signal_waves=ready, auto_focus=ready, section_ambience=ready, '
        'heading_mask=ready, cinematic_media=ready, nav_motion=ready, ripple=ready, '
        'section_beam=ready, footer_ambient=ready, scroll_depth=ready, browser_compat=ready, '
        'visibility_pause=ready, low_power_guard=ready, reduced_motion=ready'
    )


if __name__ == '__main__':
    main()
