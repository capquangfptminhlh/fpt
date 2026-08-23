from __future__ import annotations

import argparse
import re
from pathlib import Path

SITE_BASE = "/fpt"
STYLE_TAG = '<link rel="stylesheet" href="/fpt/assets/css/site-shell.css?v=20260823-1" data-site-shell-style="true"/>'
NAV_RE = re.compile(
    r'<nav\b[^>]*class=["\'][^"\']*nav-links[^"\']*["\'][^>]*>.*?</nav>',
    flags=re.I | re.S,
)

MENU = (
    ("Internet", "/fpt/internet-fpt/", "internet"),
    ("Gói cước", "/fpt/goi-cuoc-fpt/", "plans"),
    ("Combo", "/fpt/combo-fpt/", "combo"),
    ("WiFi 7", "/fpt/wifi-7/", "wifi"),
    ("Camera", "/fpt/camera-fpt/", "camera"),
    ("FPT Play", "/fpt/fpt-play/", "play"),
    ("Khu vực", "/fpt/khu-vuc/", "area"),
    ("Hỗ trợ", "/fpt/ho-tro/", "support"),
)


def active_key(rel: str) -> str | None:
    rel = rel.strip("/")
    if not rel or rel == "index.html":
        return None
    if rel.startswith("internet-fpt/") or rel.startswith("cap-quang-fpt/"):
        return "internet"
    if rel.startswith("goi-cuoc-fpt/") or rel.startswith("goi-cuoc/") or rel.startswith("bang-gia-fpt/"):
        if "/combo-" in f"/{rel}" or rel.startswith("goi-cuoc/combo-"):
            return "combo"
        return "plans"
    if rel.startswith("combo-fpt/") or rel.startswith("internet-truyen-hinh-fpt/"):
        return "combo"
    if rel.startswith("wifi-7/") or rel.startswith("wifi-fpt/") or rel.startswith("wifi-6-fpt/") or rel.startswith("mesh-wifi-fpt/") or rel.startswith("xgs-pon-fpt/"):
        return "wifi"
    if rel.startswith("camera-fpt/") or rel.startswith("giai-phap/camera/"):
        return "camera"
    if rel.startswith("fpt-play/"):
        return "play"
    if rel.startswith("khu-vuc/"):
        return "area"
    if rel.startswith("ho-tro/") or rel.startswith("lien-he/"):
        return "support"
    return None


def build_nav(active: str | None) -> str:
    links = []
    for label, href, key in MENU:
        cls = ' class="active" aria-current="page"' if key == active else ""
        links.append(f'<a{cls} href="{href}">{label}</a>')
    return '<nav class="nav-links" aria-label="Điều hướng chính">' + "".join(links) + "</nav>"


def normalize_html(text: str, rel: str) -> str:
    active = active_key(rel)
    nav = build_nav(active)
    text, nav_count = NAV_RE.subn(nav, text, count=1)
    if nav_count == 0:
        raise RuntimeError(f"missing nav-links in {rel}")

    cta = (
        '<div class="nav-cta">'
        '<a class="header-call" href="tel:19006600">1900 6600</a>'
        '<a class="header-register" href="/fpt/lien-he/">Đăng ký</a>'
        '</div>'
    )
    text = re.sub(
        r'<div\b[^>]*class=["\'][^"\']*nav-cta[^"\']*["\'][^>]*>.*?</div>',
        cta,
        text,
        count=1,
        flags=re.I | re.S,
    )

    text = re.sub(
        r'(<a\b[^>]*class=["\'][^"\']*brand[^"\']*["\'][^>]*href=)["\'][^"\']*["\']',
        r'\1"/fpt/"',
        text,
        count=1,
        flags=re.I,
    )

    if re.search(r'<body\b[^>]*class=', text, flags=re.I):
        text = re.sub(
            r'<body\b([^>]*?)class=["\']([^"\']*)["\']([^>]*)>',
            lambda m: f'<body{m.group(1)}class="{(m.group(2) + " site-shell").strip()}"{m.group(3)}>',
            text,
            count=1,
            flags=re.I,
        )
    else:
        text = re.sub(r'<body\b([^>]*)>', r'<body class="site-shell"\1>', text, count=1, flags=re.I)

    if 'data-site-shell-style=' not in text:
        text = text.replace('</head>', STYLE_TAG + '</head>', 1)
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)

    pages = sorted(site.rglob('*.html'))
    changed = 0
    errors: list[str] = []
    for page in pages:
        rel = page.relative_to(site).as_posix()
        original = page.read_text(encoding='utf-8')
        # Redirect/utility stubs may contain the string "nav-links" in scripts or comments
        # but no actual navigation element. Only normalize real nav markup.
        if not NAV_RE.search(original):
            continue
        try:
            updated = normalize_html(original, rel)
        except RuntimeError as exc:
            errors.append(str(exc))
            continue
        if updated != original:
            page.write_text(updated, encoding='utf-8')
            changed += 1

    shell = site / 'assets/css/site-shell.css'
    if not shell.exists():
        errors.append('missing assets/css/site-shell.css')

    core = [
        'index.html','internet-fpt/index.html','goi-cuoc-fpt/index.html','combo-fpt/index.html',
        'wifi-7/index.html','camera-fpt/index.html','fpt-play/index.html','khu-vuc/index.html','ho-tro/index.html'
    ]
    for rel in core:
        path = site / rel
        if not path.exists():
            errors.append(f'missing core page {rel}')
            continue
        html = path.read_text(encoding='utf-8')
        for marker in ('site-shell','data-site-shell-style=','>Internet</a>','>Gói cước</a>','>Combo</a>','>WiFi 7</a>','>Camera</a>','>FPT Play</a>','>Khu vực</a>','>Hỗ trợ</a>'):
            if marker not in html:
                errors.append(f'{rel}: missing unified shell marker {marker}')

    if errors:
        print('SITE SHELL NORMALIZE FAIL')
        for error in errors[:80]:
            print(f'- {error}')
        raise SystemExit(1)

    print(f'SITE SHELL NORMALIZE PASS: pages_changed={changed}, core_pages={len(core)}, nav=unified, theme=neo')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
