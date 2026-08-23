from __future__ import annotations

import argparse
import re
from pathlib import Path

TRANSITION_STYLE='<link rel="stylesheet" href="/fpt/assets/css/page-transition.css?v=20260817-1" data-page-transition-style="true"/>'
UI_STYLE='<link rel="stylesheet" href="/fpt/assets/css/ui-reset.css?v=20260817-1" data-ui-reset-style="true"/>'
UI_MOTION_STYLE='<link rel="stylesheet" href="/fpt/assets/css/ui-motion.css?v=20260817-1" data-ui-motion-style="true"/>'
MOBILE_PREMIUM_STYLE='<link rel="stylesheet" href="/fpt/assets/css/mobile-premium.css?v=20260823-2" data-mobile-premium-style="true"/>'
TRANSITION_SCRIPT='<script defer src="/fpt/assets/js/page-transition.js?v=20260817-2" data-page-transition-script="true"></script>'
UI_MOTION_SCRIPT='<script defer src="/fpt/assets/js/ui-motion.js?v=20260817-1" data-ui-motion-script="true"></script>'
CONTACT_SCRIPT='<script defer src="/fpt/assets/js/contact-dock.js?v=20260817-10" data-contact-dock-script="true"></script>'
LEGACY_MARKERS=('data-apple-polish-style=','data-apple-contact-style=','data-motion-system-style=','data-full-page-motion-style=','data-color-stability-style=','data-contact-dock-style=','data-mobile-stability-style=','data-mobile-contact-final-style=','data-mobile-nav-final-style=','data-motion-system-script=','data-full-page-motion-script=')

def strip_legacy_runtime_layers(html:str)->str:
    html=re.sub(r'<link\b[^>]*data-mobile-v3=["\'][^"\']*["\'][^>]*/?>','',html,flags=re.I)
    html=re.sub(r'<link\b[^>]*data-mobile-premium-style=["\'][^"\']*["\'][^>]*/?>','',html,flags=re.I)
    return html

def inject(html:str)->str:
    if 'fpt-match-v2' in html:
        # Match v2 owns its header, mobile behavior and contact dock. Any global injection changes the approved render.
        return html
    if '</head>' not in html: raise ValueError('missing </head>')
    if '</body>' not in html: raise ValueError('missing </body>')
    html=strip_legacy_runtime_layers(html)
    if any(marker in html for marker in LEGACY_MARKERS): raise ValueError('legacy injected UI marker found in source HTML')
    head_assets=[]
    if 'data-page-transition-style=' not in html: head_assets.append(TRANSITION_STYLE)
    if 'data-ui-reset-style=' not in html: head_assets.append(UI_STYLE)
    if 'data-ui-motion-style=' not in html: head_assets.append(UI_MOTION_STYLE)
    head_assets.append(MOBILE_PREMIUM_STYLE)
    html=html.replace('</head>',''.join(head_assets)+'</head>',1)
    body_assets=[]
    if 'data-page-transition-script=' not in html: body_assets.append(TRANSITION_SCRIPT)
    if 'data-ui-motion-script=' not in html: body_assets.append(UI_MOTION_SCRIPT)
    if 'data-contact-dock-script=' not in html: body_assets.append(CONTACT_SCRIPT)
    if body_assets: html=html.replace('</body>',''.join(body_assets)+'</body>',1)
    return html

def main()->None:
    parser=argparse.ArgumentParser(); parser.add_argument('--site',required=True); args=parser.parse_args(); site=Path(args.site)
    pages=sorted(site.rglob('*.html'))
    if not pages: raise SystemExit('No HTML pages found')
    changed=0; preserved=0
    for page in pages:
        old=page.read_text(encoding='utf-8')
        if 'fpt-match-v2' in old: preserved+=1
        new=inject(old)
        if new!=old: page.write_text(new,encoding='utf-8'); changed+=1
    print(f'UI runtime injected: pages={len(pages)}, changed={changed}, match_v2_preserved={preserved}')

if __name__=='__main__': main()
