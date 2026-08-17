from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument('--site', required=True); args = parser.parse_args()
    site = Path(args.site); pages = sorted(site.rglob('*.html')); errors: list[str] = []
    polish = (site/'assets/css/apple-polish.css').read_text(encoding='utf-8')
    contact = (site/'assets/css/apple-contact.css').read_text(encoding='utf-8')
    dock = (site/'assets/css/contact-dock.css').read_text(encoding='utf-8')
    for token in (':root{','.topbar{','.home-v2 .m-hero h1{','.seo-hero{','.footer,.home-v2 .footer{','@media(max-width:760px)'):
        if token not in polish: errors.append(f'apple-polish missing {token}')
    for token in ('.contact-hero{','.lead-card{','.contact-section{','.contact-callout{'):
        if token not in contact: errors.append(f'apple-contact missing {token}')
    for token in ('.contact-dock{','.contact-dock .contact-copy{','.contact-dock .contact-copy strong{','.contact-dock .contact-copy small{','.contact-zalo{--accent:#0068ff','.contact-call{--accent:#19a45a','.contact-register{--accent:#f37021','grid-template-columns:repeat(3,minmax(0,1fr))!important','@media(prefers-reduced-motion:reduce)'):
        if token not in dock: errors.append(f'contact-dock missing {token}')
    if '\n.contact-copy{' in dock or '\n.contact-copy strong{' in dock or '\n.contact-copy small{' in dock:
        errors.append('contact dock contains unscoped .contact-copy selector')
    combined=(polish+'\n'+contact+'\n'+dock).lower()
    for token in ('@import url(','fonts.googleapis.com','use.typekit.net'):
        if token in combined: errors.append(f'external font forbidden: {token}')
    tagged=dock_ok=0
    for page in pages:
        html=page.read_text(encoding='utf-8'); rel=page.relative_to(site)
        if 'data-apple-polish-style=' not in html or 'data-apple-contact-style=' not in html: errors.append(f'{rel}: missing polish assets')
        else: tagged += 1
        if 'contact-dock.css?v=20260817-12' not in html or 'contact-dock.js?v=20260817-10' not in html: errors.append(f'{rel}: missing scoped dock assets')
        else: dock_ok += 1
    if errors:
        print('VISUAL QA FAIL'); [print(f'- {e}') for e in errors[:100]]; raise SystemExit(1)
    print(f'VISUAL QA PASS: pages={len(pages)}, polish={tagged}, scoped_dock={dock_ok}, selector_collision=0, external_fonts=0')


if __name__ == '__main__': main()
