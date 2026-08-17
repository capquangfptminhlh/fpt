from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

SITE_BASE = '/fpt'
REQUIRED_CONTACT = (
    'https://zalo.me/fpttelecom',
    "phone: '19006600'",
    "sitePath('/lien-he/')",
    'data-contact-action="zalo" data-no-transition',
    'data-contact-action="call" data-no-transition',
    'contact-icon contact-icon-zalo',
    'contact-icon contact-icon-call',
    'contact-icon contact-icon-register',
    '<span>Zalo</span>',
)
REQUIRED_TRANSITION_JS = (
    "prefers-reduced-motion: reduce",
    "sessionStorage",
    "next.origin !== location.origin",
    "pageshow",
    "FPTPageTransition",
    "mailto:|tel:|javascript:",
    "anchor.hasAttribute('data-no-transition')",
)

class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(); self.links=[]; self.scripts=[]; self.styles=[]; self.forms=0
    def handle_starttag(self, tag, attrs):
        data=dict(attrs)
        if tag=='a' and data.get('href'): self.links.append(data['href'] or '')
        elif tag=='script' and data.get('src'): self.scripts.append(data['src'] or '')
        elif tag=='link' and data.get('href') and 'stylesheet' in (data.get('rel') or ''): self.styles.append(data['href'] or '')
        elif tag=='form': self.forms += 1

def local_target(site: Path, html_file: Path, href: str) -> Path | None:
    href=href.strip()
    if not href or href.startswith(('#','http://','https://','mailto:','tel:','javascript:')): return None
    path=urlsplit(href).path
    if not path: return None
    if path in (SITE_BASE,f'{SITE_BASE}/'): return site/'index.html'
    if path.startswith(f'{SITE_BASE}/'): target=site/path[len(SITE_BASE)+1:]
    elif path.startswith('/'): target=site/path[1:]
    else: target=html_file.parent/path
    target=target.resolve()
    if target.is_dir() or path.endswith('/'): target=target/'index.html'
    return target

def is_legacy_redirect(text: str) -> bool:
    low=text.lower(); return 'name="robots" content="noindex,follow"' in low and 'http-equiv="refresh"' in low

def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--site',required=True); args=parser.parse_args()
    site=Path(args.site).resolve(); pages=sorted(site.rglob('*.html')); errors=[]; checked_links=0; legacy_redirects=0
    if len(pages)<70: errors.append(f'Expected >=70 HTML pages, found {len(pages)}')
    for page in pages:
        text=page.read_text(encoding='utf-8'); parsed=PageParser(); parsed.feed(text); rel=page.relative_to(site); legacy=is_legacy_redirect(text)
        if legacy: legacy_redirects += 1
        if not legacy and 'assets/js/main.js' not in text: errors.append(f'{rel}: missing main.js')
        for marker,label in (('data-contact-dock-style=','contact dock stylesheet'),('data-contact-dock-script=','contact dock script'),('data-page-transition-style=','page transition stylesheet'),('data-page-transition-script=','page transition script')):
            if marker not in text: errors.append(f'{rel}: missing {label}')
        for href in parsed.links:
            if href.startswith(('http://','https://','mailto:','tel:','javascript:','#')): continue
            checked_links += 1; target=local_target(site,page,href)
            if target is None: continue
            try: target.relative_to(site)
            except ValueError: errors.append(f'{rel}: link escapes site root: {href}'); continue
            if not target.exists(): errors.append(f'{rel}: broken internal link: {href}')
    contact_js=site/'assets/js/contact-dock.js'
    if not contact_js.exists(): errors.append('Missing assets/js/contact-dock.js')
    else:
        contact_text=contact_js.read_text(encoding='utf-8')
        for required in REQUIRED_CONTACT:
            if required not in contact_text: errors.append(f'contact-dock.js missing required action config: {required}')
        if 'target="_blank"' in contact_text: errors.append('contact-dock.js must not force Zalo into a new tab')
        for action in ('zalo','call','register'):
            if f'data-contact-action="{action}"' not in contact_text: errors.append(f'contact-dock.js missing rendered action: {action}')
    transition_js=site/'assets/js/page-transition.js'; transition_css=site/'assets/css/page-transition.css'
    if not transition_js.exists(): errors.append('Missing assets/js/page-transition.js')
    else:
        transition_text=transition_js.read_text(encoding='utf-8')
        for required in REQUIRED_TRANSITION_JS:
            if required not in transition_text: errors.append(f'page-transition.js missing behavior guard: {required}')
        if 'page-transition__modem' not in transition_text or 'page-transition__waves' not in transition_text: errors.append('page-transition.js missing modem/wifi loader markup')
    if not transition_css.exists(): errors.append('Missing assets/css/page-transition.css')
    else:
        transition_style=transition_css.read_text(encoding='utf-8')
        for required in ('.page-transition','@media(prefers-reduced-motion:reduce)','@keyframes modem-run','@keyframes wifi-wave'):
            if required not in transition_style: errors.append(f'page-transition.css missing animation/accessibility rule: {required}')
    contact_css=site/'assets/css/contact-dock.css'
    if not contact_css.exists(): errors.append('Missing assets/css/contact-dock.css')
    else:
        style=contact_css.read_text(encoding='utf-8')
        for required in ('touch-action:manipulation','z-index:2147482000','.contact-dock .contact-action{','.contact-dock .contact-copy{','@media(max-width:760px)'):
            if required not in style: errors.append(f'contact-dock.css missing scoped interaction guard: {required}')
        if '\n.contact-copy{' in style: errors.append('contact-dock.css leaks unscoped .contact-copy')
    lead_page=site/'lien-he/index.html'; lead_js=site/'assets/js/lead-form.js'
    if not lead_page.exists(): errors.append('Missing lien-he/index.html')
    else:
        lead_text=lead_page.read_text(encoding='utf-8')
        if 'data-lead-form' not in lead_text: errors.append('Contact page missing data-lead-form')
        if 'assets/js/lead-form.js' not in lead_text: errors.append('Contact page missing lead-form.js')
    if not lead_js.exists(): errors.append('Missing assets/js/lead-form.js')
    else:
        lead_text=lead_js.read_text(encoding='utf-8')
        if 'email.gosecureserver.in/api/send.php' not in lead_text: errors.append('Lead JS missing production endpoint')
        if 'hp_email' not in lead_text: errors.append('Lead JS missing honeypot payload')
        if not re.search(r'\bresponse\.ok\b',lead_text): errors.append('Lead JS missing HTTP success validation')
    if errors:
        print('FUNCTIONAL QA FAIL'); [print(f'- {item}') for item in errors[:80]]; raise SystemExit(1)
    print(f'FUNCTIONAL QA PASS: pages={len(pages)}, internal_links={checked_links}, legacy_redirects={legacy_redirects}, contact_actions=3, direct_contact=ready, lead_form=ready, modem_transition=ready')

if __name__=='__main__': main()
