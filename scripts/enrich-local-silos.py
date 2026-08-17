from __future__ import annotations

import argparse
import json
import os
import re
from html import escape, unescape
from pathlib import Path

ORIGIN = "https://your-domain.example"
ADMIN_SOURCE = "https://xaydungchinhsach.chinhphu.vn/chi-tiet-34-don-vi-hanh-chinh-cap-tinh-tu-12-6-2025-119250612141845533.htm"
FPT_SOURCE = "https://fpt.vn/vi/"

INTERNET = [
    ("Giga", "goi-cuoc/giga/", "Gói Internet FPT cho nhu cầu gia đình phổ thông."),
    ("Sky", "goi-cuoc/sky/", "Gói Internet FPT cho nhu cầu sử dụng nhiều thiết bị."),
    ("Meta", "goi-cuoc/meta/", "Gói Internet FPT cho nhu cầu kết nối cao hơn."),
    ("F-Game", "goi-cuoc/f-game/", "Gói Internet hướng tới game và kết nối cần độ ổn định."),
    ("SpeedX2", "goi-cuoc/speedx2/", "Dòng SpeedX cho nhu cầu hiệu năng cao."),
    ("SpeedX2 Pro", "goi-cuoc/speedx2-pro/", "Phiên bản Pro trong dòng SpeedX."),
    ("SpeedX10", "goi-cuoc/speedx10/", "Dòng SpeedX cho nhu cầu kết nối chuyên sâu."),
    ("SpeedX10 Pro", "goi-cuoc/speedx10-pro/", "Phiên bản Pro trong dòng SpeedX hiệu năng cao."),
]

PLAY = [
    ("Combo Giga + FPT Play", "goi-cuoc/combo-giga/", "Internet kết hợp nội dung FPT Play."),
    ("Combo Sky + FPT Play", "goi-cuoc/combo-sky/", "Internet kết hợp FPT Play cho gia đình nhiều thiết bị."),
    ("Combo Meta + FPT Play", "goi-cuoc/combo-meta/", "Internet và FPT Play trong cùng nhóm nhu cầu."),
    ("Combo F-Game + FPT Play", "goi-cuoc/combo-f-game/", "Internet định hướng game kết hợp FPT Play."),
    ("FPT Play", "fpt-play/", "Trang dịch vụ truyền hình và giải trí FPT Play."),
]

CAMERA = [
    ("Camera FPT", "camera-fpt/", "Trang tổng quan giải pháp Camera FPT."),
    ("Camera Play 3", "camera-fpt/play-3/", "Trang sản phẩm Camera Play 3 hiện có trên website."),
    ("Camera Play 4", "camera-fpt/play-4/", "Trang sản phẩm Camera Play 4 hiện có trên website."),
]


def schema_json(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def text_name(html: str, path: Path) -> str:
    match = re.search(r"<h1[^>]*>\s*Lắp mạng FPT tại\s+(.*?)</h1>", html, flags=re.I | re.S)
    if not match:
        raise SystemExit(f"LOCAL SILO BUILD FAIL: cannot read location name from {path}")
    return re.sub(r"<[^>]+>", "", unescape(match.group(1))).strip()


def cards(items, prefix: str, product_type: str) -> str:
    out = []
    for title, url, desc in items:
        out.append(
            f'<a class="link-tile" data-local-product="{product_type}" href="{prefix}{url}">'
            f'<strong>{escape(title)}</strong><span>{escape(desc)} Chi tiết áp dụng cần kiểm tra theo địa chỉ.</span></a>'
        )
    return "".join(out)


def catalog_section(name: str) -> str:
    return f'''<section class="section" id="goi-dich-vu-dia-phuong"><div class="container">
<div class="section-head"><span class="eyebrow">Danh mục dịch vụ tại {escape(name)}</span><h2>Internet, truyền hình FPT Play và Camera</h2><p>Danh mục dưới đây bao phủ toàn bộ trang gói/sản phẩm đang có trên website. Tên gói là đường dẫn tham khảo; giá, thiết bị, ưu đãi và khả năng triển khai tại {escape(name)} chỉ được xác nhận sau khi kiểm tra địa chỉ.</p></div>
<div class="content-card"><h2>Đủ gói Internet FPT</h2><div class="link-grid">{cards(INTERNET, '../../', 'internet')}</div></div>
<div class="content-card" style="margin-top:24px"><h2>Internet + Truyền hình FPT Play</h2><div class="link-grid">{cards(PLAY, '../../', 'play')}</div></div>
<div class="content-card" style="margin-top:24px"><h2>Camera FPT</h2><div class="link-grid">{cards(CAMERA, '../../', 'camera')}</div></div>
<div class="hold-local" style="margin-top:24px"><strong>Nguyên tắc địa phương:</strong> Không lấy một mức giá, khuyến mãi, thiết bị hoặc kết luận hạ tầng chung cho toàn {escape(name)}. Hãy mở trang gói để xem đặc tính, sau đó gửi địa chỉ thực tế để đối chiếu điều kiện đang áp dụng.</div>
<div class="cta-row" style="margin-top:24px"><a class="btn btn-primary" href="#dang-ky">Kiểm tra gói theo địa chỉ</a><a class="btn btn-secondary" data-local-news-link href="tin-tuc/">Tin tức {escape(name)}</a></div>
</div></section>'''


def render_news(name: str, slug: str) -> str:
    desc = f"Tin tức FPT tại {name}: nơi tập hợp cập nhật Internet, FPT Play, Camera và hướng dẫn địa phương có nguồn kiểm chứng."
    page = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": f"Tin tức FPT {name}",
        "url": f"{ORIGIN}/khu-vuc/{slug}/tin-tuc/",
        "description": desc,
        "about": ["Internet FPT", "FPT Play", "Camera FPT", name],
    }
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Trang chủ", "item": ORIGIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "Khu vực", "item": ORIGIN + "/khu-vuc/"},
            {"@type": "ListItem", "position": 3, "name": name, "item": f"{ORIGIN}/khu-vuc/{slug}/"},
            {"@type": "ListItem", "position": 4, "name": "Tin tức"},
        ],
    }
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Tin tức FPT {escape(name)} – Internet, FPT Play, Camera</title><meta name="description" content="{escape(desc)}"/><link rel="canonical" href="{ORIGIN}/khu-vuc/{slug}/tin-tuc/"/><meta name="robots" content="index,follow,max-image-preview:large"/><meta property="og:title" content="Tin tức FPT {escape(name)}"/><meta property="og:description" content="{escape(desc)}"/><meta property="og:type" content="website"/><meta property="og:url" content="{ORIGIN}/khu-vuc/{slug}/tin-tuc/"/><meta property="og:image" content="{ORIGIN}/assets/images/seo/khu-vuc-body.webp"/><link rel="stylesheet" href="../../../assets/css/styles.css"/><script type="application/ld+json">{schema_json(page)}</script><script type="application/ld+json">{schema_json(crumbs)}</script></head>
<body class="local-news-page"><header class="topbar"><div class="container nav"><a class="brand" href="../../../index.html"><img src="../../../assets/images/logo-fpt.svg" width="180" height="48" alt="FPT Telecom"/></a><button class="mobile-toggle" aria-label="Mở menu">☰</button><nav class="nav-links" aria-label="Điều hướng chính"><a href="../../../index.html">Trang chủ</a><a href="../../../lap-mang-fpt/">Lắp mạng</a><a href="../../../goi-cuoc-fpt/">Gói cước</a><a href="../../../fpt-play/">FPT Play</a><a href="../../../camera-fpt/">Camera</a><a href="../../../tin-tuc/">Tin tức chung</a></nav><div class="nav-cta"><a class="hotline" href="tel:19006600">1900 6600 · CSKH</a></div></div></header>
<main><section class="seo-hero"><img src="../../../assets/images/seo/khu-vuc-body.webp" width="1600" height="900" fetchpriority="high" alt="Tin tức FPT tại {escape(name)}"/><div class="container inner"><div class="breadcrumbs"><a href="../../../index.html">Trang chủ</a><span>›</span><a href="../../">Khu vực</a><span>›</span><a href="../">{escape(name)}</a><span>›</span><span>Tin tức</span></div><h1>Tin tức FPT tại {escape(name)}</h1><p>Cập nhật Internet, FPT Play, Camera và hướng dẫn địa phương theo nguyên tắc chỉ xuất bản thông tin có nguồn kiểm chứng.</p><div class="cta-row"><a class="btn btn-primary" href="../#dang-ky">Kiểm tra theo địa chỉ</a><a class="btn btn-secondary" href="../#goi-dich-vu-dia-phuong">Xem đủ gói tại {escape(name)}</a></div></div></section>
<section class="section"><div class="container content-grid"><article class="content-card"><span class="eyebrow">Tin tức địa phương</span><h2>Cập nhật dành riêng cho {escape(name)}</h2><div class="hold-local"><strong>Tin địa phương chỉ xuất bản khi có nguồn.</strong> Không tạo bài đổi tên tỉnh, không suy diễn khuyến mãi, giá, sự cố, lịch bảo trì hoặc phạm vi hạ tầng nếu chưa có bằng chứng theo địa bàn và thời điểm.</div><h3>Nhóm nội dung sẽ được cập nhật</h3><ul><li>Thông báo hoặc thay đổi có nguồn liên quan Internet FPT tại {escape(name)}.</li><li>Thông tin FPT Play, truyền hình và nội dung áp dụng có căn cứ.</li><li>Camera FPT, thiết bị và hướng dẫn lắp đặt phù hợp nhu cầu địa phương.</li><li>Cẩm nang ghi địa chỉ sau thay đổi hành chính để kiểm tra chính xác hơn.</li></ul><p>Hiện tại trang này đóng vai trò hub địa phương. Bài mới chỉ được đưa vào khi có nguồn đủ mạnh và qua kiểm tra trùng lặp/cannibalization.</p></article><aside class="content-card"><span class="eyebrow">Đi nhanh</span><h2 style="font-size:26px">Dịch vụ tại {escape(name)}</h2><div class="link-grid" style="grid-template-columns:1fr"><a class="link-tile" href="../#goi-dich-vu-dia-phuong"><strong>Internet FPT</strong><span>Đủ nhóm gói đang có trên website</span></a><a class="link-tile" href="../../../fpt-play/"><strong>FPT Play</strong><span>Truyền hình và giải trí</span></a><a class="link-tile" href="../../../camera-fpt/"><strong>Camera FPT</strong><span>Camera và giám sát</span></a><a class="link-tile" href="../"><strong>Trang {escape(name)}</strong><span>Kiểm tra địa chỉ và gửi yêu cầu</span></a></div></aside></div></section>
<section class="section"><div class="container"><div class="content-card"><span class="eyebrow">Nguồn &amp; kiểm chứng</span><h2>Nguyên tắc biên tập local</h2><p>Địa giới hành chính được đối chiếu với công bố của Báo Điện tử Chính phủ. Các thông tin sản phẩm/dịch vụ cần đối chiếu nguồn FPT Telecom và điều kiện tại địa chỉ trước khi biến thành claim địa phương.</p><p><a href="{ADMIN_SOURCE}" rel="nofollow noopener" target="_blank">Nguồn địa giới hành chính</a> · <a href="{FPT_SOURCE}" rel="nofollow noopener" target="_blank">FPT Telecom</a></p></div></div></section></main>
<footer class="footer"><div class="container footer-grid"><div><img src="../../../assets/images/logo-fpt.svg" width="180" height="48" alt="FPT Telecom" style="height:36px;margin-bottom:12px"/><p>Hub tin tức địa phương phục vụ SEO/AEO/GEO theo nguyên tắc có bằng chứng.</p></div><div><h3>Khu vực</h3><ul><li><a href="../">{escape(name)}</a></li><li><a href="../../">34 tỉnh/thành</a></li></ul></div><div><h3>Dịch vụ</h3><ul><li><a href="../../../goi-cuoc-fpt/">Internet</a></li><li><a href="../../../fpt-play/">FPT Play</a></li><li><a href="../../../camera-fpt/">Camera</a></li></ul></div><div><h3>Đăng ký</h3><a class="btn btn-primary" href="../#dang-ky">Kiểm tra địa chỉ</a></div></div></footer><script src="../../../assets/js/main.js"></script></body></html>'''


def insert_catalog(path: Path) -> tuple[str, str]:
    html = path.read_text(encoding="utf-8")
    name = text_name(html, path)
    if 'id="goi-dich-vu-dia-phuong"' not in html:
        marker = '<section class="contact-section soft" id="dang-ky">'
        if marker not in html:
            raise SystemExit(f"LOCAL SILO BUILD FAIL: contact marker missing in {path}")
        html = html.replace(marker, catalog_section(name) + "\n" + marker, 1)
        path.write_text(html, encoding="utf-8")
    return name, path.parent.name


def enrich_hub(hub: Path, locations: list[tuple[str, str]]) -> None:
    html = hub.read_text(encoding="utf-8")
    if 'id="tin-tuc-theo-tinh"' in html:
        return
    links = "".join(
        f'<a class="link-tile" href="{escape(slug)}/tin-tuc/"><strong>Tin tức {escape(name)}</strong><span>Internet · FPT Play · Camera</span></a>'
        for name, slug in locations
    )
    block = f'''<section class="section" id="tin-tuc-theo-tinh"><div class="container"><div class="section-head"><span class="eyebrow">Tin tức địa phương</span><h2>Tin tức theo 34 tỉnh/thành</h2><p>Mỗi tỉnh/thành có một hub tin tức riêng. Chỉ xuất bản bài có nguồn kiểm chứng; không tạo hàng loạt bài đổi tên địa phương.</p></div><div class="link-grid">{links}</div></div></section>'''
    if "</main>" not in html:
        raise SystemExit("LOCAL SILO BUILD FAIL: hub missing </main>")
    hub.write_text(html.replace("</main>", block + "</main>", 1), encoding="utf-8")


def add_khu_vuc_nav(site: Path) -> int:
    changed = 0
    for path in site.rglob("*.html"):
        html = path.read_text(encoding="utf-8")
        if "nav-links" not in html or re.search(r">\s*Khu vực\s*</a>", html, flags=re.I):
            continue
        rel = Path(os.path.relpath(site / "khu-vuc", path.parent)).as_posix()
        href = (rel.rstrip("/") + "/") if rel != "." else "./"
        nav_match = re.search(r'(<nav\b[^>]*class=["\'][^"\']*nav-links[^"\']*["\'][^>]*>.*?)(</nav>)', html, flags=re.I | re.S)
        if not nav_match:
            continue
        replacement = nav_match.group(1) + f'<a href="{href}">Khu vực</a>' + nav_match.group(2)
        html = html[:nav_match.start()] + replacement + html[nav_match.end():]
        path.write_text(html, encoding="utf-8")
        changed += 1
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True)
    args = parser.parse_args()
    site = Path(args.site)
    local_root = site / "khu-vuc"
    if not local_root.exists():
        raise SystemExit("LOCAL SILO BUILD FAIL: khu-vuc missing")

    locations: list[tuple[str, str]] = []
    for page in sorted(local_root.glob("*/index.html")):
        name, slug = insert_catalog(page)
        locations.append((name, slug))
        news = page.parent / "tin-tuc" / "index.html"
        news.parent.mkdir(parents=True, exist_ok=True)
        news.write_text(render_news(name, slug), encoding="utf-8")

    if len(locations) != 34:
        raise SystemExit(f"LOCAL SILO BUILD FAIL: expected 34 locations, got {len(locations)}")

    enrich_hub(local_root / "index.html", locations)
    nav_changed = add_khu_vuc_nav(site)
    print(f"Local silos enriched: 34 catalogs + 34 news hubs; Khu vực nav injected on {nav_changed} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
