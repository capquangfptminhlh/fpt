from __future__ import annotations

import argparse
from pathlib import Path

TRUST_BLOCK = '''<div class="container site-trust-links" data-site-trust-links="v1" style="padding:16px 0 0;margin-top:16px;border-top:1px solid rgba(148,163,184,.22);font-size:13px;line-height:1.7"><span style="opacity:.78">Minh bạch nội dung:</span> <a href="/fpt/gioi-thieu/">Giới thiệu</a> · <a href="/fpt/phuong-phap-bien-tap/">Phương pháp biên tập</a> · <a href="/fpt/chinh-sach-cap-nhat/">Chính sách cập nhật</a> · <a href="/fpt/lien-he/">Liên hệ</a></div>'''


def inject(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    if 'data-site-trust-links="v1"' in html:
        return False
    if '</footer>' in html:
        html = html.replace('</footer>', TRUST_BLOCK + '</footer>', 1)
    elif '</body>' in html:
        html = html.replace('</body>', TRUST_BLOCK + '</body>', 1)
    else:
        raise SystemExit(f"TRUST FOOTER BUILD FAIL: no footer/body close in {path}")
    path.write_text(html, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    pages = sorted(site.rglob('*.html'))
    if not pages:
        raise SystemExit('TRUST FOOTER BUILD FAIL: no HTML pages found')
    changed = sum(1 for page in pages if inject(page))
    print(f'TRUST FOOTER BUILT: pages={len(pages)}, injected={changed}; about + methodology + freshness + contact linked sitewide')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
