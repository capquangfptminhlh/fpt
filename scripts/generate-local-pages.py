from __future__ import annotations

import argparse
import json
import re
from html import escape
from pathlib import Path

SITE_ORIGIN = "https://capquangfptminhlh.github.io/fpt"
UPDATED = "2026-08-17"


def load_provinces(root: Path) -> dict:
    return json.loads((root / "data" / "local-provinces.json").read_text(encoding="utf-8"))


def nav_html() -> str:
    return '''<header class="topbar"><div class="container nav">
<a class="brand" href="/fpt/"><img alt="FPT Telecom" decoding="async" height="48" src="/fpt/assets/images/logo-fpt.svg" width="180"/></a>
<button aria-label="Mở menu" class="mobile-toggle">☰</button>
<nav class="nav-links"><a href="/fpt/">Trang chủ</a><a href="/fpt/lap-mang-fpt/">Lắp mạng FPT</a><a href="/fpt/goi-cuoc-fpt/">Gói cước</a><a href="/fpt/giai-phap/">Giải pháp</a><a href="/fpt/so-sanh/">So sánh</a><a href="/fpt/ho-tro/">Hỗ trợ</a><a href="/fpt/kien-thuc/">Kiến thức</a><a href="/fpt/khu-vuc/">Khu vực</a></nav>
<div class="nav-cta"><a class="hotline" href="tel:19006600">1900 6600</a></div>
</div></header>'''


def footer_html() -> str:
    return '''<footer class="footer"><div class="container footer-grid">
<div><img alt="FPT Telecom" decoding="async" height="48" src="/fpt/assets/images/logo-fpt.svg" style="height:36px;margin-bottom:12px" width="180"/><p>Website tư vấn độc lập, tổng hợp thông tin công khai để hỗ trợ chọn Internet FPT theo nhu cầu.</p><p>Giá, ưu đãi, thiết bị và khả năng triển khai cần được xác minh theo địa chỉ trước khi đăng ký.</p></div>
<div><h3>Internet FPT</h3><ul><li><a href="/fpt/lap-mang-fpt/">Lắp mạng FPT</a></li><li><a href="/fpt/goi-cuoc-fpt/">Gói cước FPT</a></li><li><a href="/fpt/combo-fpt/">Combo FPT</a></li><li><a href="/fpt/speedx-fpt/">SpeedX</a></li></ul></div>
<div><h3>Giải pháp</h3><ul><li><a href="/fpt/giai-phap/gia-dinh/">Gia đình</a></li><li><a href="/fpt/giai-phap/game-thu/">Game thủ</a></li><li><a href="/fpt/giai-phap/van-phong/">Văn phòng</a></li><li><a href="/fpt/giai-phap/nha-nhieu-tang/">Nhà nhiều tầng</a></li></ul></div>
<div><h3>Kiến thức & hỗ trợ</h3><ul><li><a href="/fpt/ho-tro/">Hỗ trợ</a></li><li><a href="/fpt/kien-thuc/">Kiến thức</a></li><li><a href="/fpt/so-sanh/">So sánh</a></li><li><a href="/fpt/khu-vuc/">Khu vực</a></li></ul></div>
<div><h3>Đăng ký</h3><a class="btn btn-primary" href="/fpt/lien-he/">Gửi yêu cầu</a><p style="margin-top:10px">Cập nhật: 17/08/2026</p></div>
</div><div class="container" style="padding-top:16px;border-top:1px solid rgba(255,255,255,.12);margin-top:18px;font-size:13px">© 2026 • Nội dung tư vấn độc lập, không cam kết giá hoặc hạ tầng trước khi xác minh địa chỉ.</div></footer>'''


def admin_copy(p: dict) -> str:
    merged = p["merged_from"]
    if len(merged) > 1:
        names = ", ".join(escape(x) for x in merged)
        return (
            f'Theo danh mục hành chính hiện hành, <strong>{escape(p["name"])}</strong> có mã cấp tỉnh '
            f'<strong>{escape(p["code"])}</strong>. Đơn vị hiện hành được hình thành từ {names}. '
            'Vì vậy trang này gom cả các truy vấn theo tên hiện hành và tên địa phương trước sắp xếp về một URL canonical, '
            'tránh tạo nhiều trang trùng ý định.'
        )
    return (
        f'Theo danh mục hành chính hiện hành, <strong>{escape(p["name"])}</strong> có mã cấp tỉnh '
        f'<strong>{escape(p["code"])}</strong>. Tên đơn vị cấp tỉnh này được giữ trong cấu trúc 34 tỉnh/thành hiện hành. '
        'Trang tập trung vào việc kiểm tra nhu cầu và địa chỉ thay vì suy diễn rằng mọi khu vực trong tỉnh/thành đều có cùng hạ tầng, giá hoặc thiết bị.'
    )


def alias_section(p: dict) -> str:
    legacy = [x for x in p["merged_from"] if x != p["name"]]
    extras = [x for x in p["aliases"] if x not in p["merged_from"]]
    items = []
    if legacy:
        items.append("<p>Nếu bạn vẫn tìm theo tên địa phương trước sắp xếp, các truy vấn sau được quy về trang này:</p>")
        items.append("<ul>" + "".join(f"<li>Lắp mạng FPT {escape(x)} → {escape(p['name'])}</li>" for x in legacy) + "</ul>")
    if extras:
        items.append("<p>Các cách gọi/viết tắt thường gặp được nhận diện cho mục đích tìm kiếm: " + ", ".join(escape(x) for x in extras) + ".</p>")
    if not items:
        items.append("<p>Trang này dùng chính tên tỉnh/thành hiện hành làm owner cho nhóm truy vấn local, không tạo thêm URL đồng nghĩa.</p>")
    return "".join(items)


def variant_intro(p: dict) -> tuple[str, str]:
    variants = [
        ("Bắt đầu từ địa chỉ lắp đặt", "Hai nhà ở cùng một tỉnh/thành vẫn có thể khác nhau về tuyến cáp, điều kiện thi công, thiết bị đi kèm và chính sách tại thời điểm đăng ký. Vì vậy bước đầu tiên là xác minh địa chỉ, sau đó mới chọn gói."),
        ("Bắt đầu từ số người và thiết bị", "Tên gói hoặc mức Mbps chỉ là một phần của quyết định. Hãy đếm số điện thoại, TV, laptop, camera, máy chơi game và thiết bị IoT thường hoạt động đồng thời rồi mới đối chiếu gói phù hợp."),
        ("Bắt đầu từ vùng phủ WiFi trong nhà", "Tốc độ đường truyền cao không tự động giải quyết điểm chết WiFi. Cần xem diện tích, số tầng, tường/vật cản và vị trí modem để quyết định có cần Mesh hoặc điểm phát bổ sung hay không."),
        ("Bắt đầu từ nhu cầu upload và độ ổn định", "Nếu nhà có camera cloud, họp video, livestream hoặc tải dữ liệu lên thường xuyên, hãy xem cả upload, độ trễ và cách bố trí mạng nội bộ thay vì chỉ nhìn tốc độ download."),
    ]
    return variants[int(p["code"]) % len(variants)]


def render_page(p: dict, data: dict) -> str:
    name = escape(p["name"])
    seo_name = escape(p.get("seo_name") or p["name"])
    slug = p["slug"]
    url = f"{SITE_ORIGIN}/khu-vuc/{slug}/"
    title = f"Lắp mạng FPT {seo_name}: kiểm tra hạ tầng & chọn gói"
    desc = f"Tư vấn lắp mạng FPT tại {p['name']}: kiểm tra hạ tầng theo địa chỉ, chọn Internet/WiFi/Camera theo nhu cầu. Giá và ưu đãi cần xác minh trước đăng ký."
    core_keywords = [f"lắp mạng fpt {p['name'].lower()}", f"internet fpt {p['name'].lower()}", f"wifi fpt {p['name'].lower()}", f"gói cước fpt {p['name'].lower()}", f"camera fpt {p['name'].lower()}", f"kiểm tra hạ tầng fpt {p['name'].lower()}"]
    intro_h2, intro_text = variant_intro(p)
    admin_source = escape(data["admin_source"], quote=True)
    code_source = escape(data["code_source"], quote=True)
    merged_q = (f"Trang này có áp dụng cho khu vực {', '.join(x for x in p['merged_from'] if x != p['name'])} không?" if len(p["merged_from"]) > 1 else f"Trang này có khẳng định mọi địa chỉ tại {p['name']} đều lắp được FPT không?")
    merged_a = (f"Các tên địa phương trước sắp xếp được map về URL {p['name']} hiện hành để tra cứu. Tuy nhiên khả năng lắp đặt vẫn phải xác minh theo địa chỉ cụ thể." if len(p["merged_from"]) > 1 else f"Không. Trang chỉ cung cấp hướng dẫn chọn dịch vụ và quy trình kiểm tra; khả năng triển khai tại {p['name']} phải xác minh theo địa chỉ cụ thể.")
    faqs = [
        (f"Lắp mạng FPT tại {p['name']} cần chuẩn bị gì?", "Chuẩn bị địa chỉ lắp đặt, số điện thoại liên hệ, nhu cầu chính, số thiết bị và thông tin về diện tích/số tầng. Không cần gửi mật khẩu, OTP, thông tin thanh toán hoặc giấy tờ định danh qua form tư vấn ban đầu."),
        (f"Giá Internet FPT tại {p['name']} có giống mọi khu vực không?", "Không nên coi một mức giá tham khảo là cam kết áp dụng cho mọi địa chỉ. Giá, ưu đãi, thiết bị và điều kiện triển khai có thể thay đổi theo khu vực, hạ tầng và thời điểm."),
        (merged_q, merged_a),
        (f"Nên chọn WiFi 6, WiFi 7 hay Mesh tại {p['name']}?", "Hãy chọn theo diện tích, số tầng, vật cản, số thiết bị và nhu cầu thực tế. Mesh phù hợp khi cần mở rộng vùng phủ; chuẩn WiFi mới hơn chỉ phát huy tốt khi thiết bị đầu cuối và môi trường sử dụng phù hợp."),
        (f"Có thể đăng ký tư vấn FPT tại {p['name']} ở đâu?", "Bạn có thể dùng form kiểm tra theo địa chỉ trên website này hoặc liên hệ kênh hỗ trợ FPT. Website này là kênh tư vấn độc lập và không tự nhận là website doanh nghiệp FPT."),
    ]
    faq_json = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    webpage_json = {"@context":"https://schema.org","@type":"WebPage","name":title,"description":desc,"url":url,"inLanguage":"vi-VN","dateModified":UPDATED,"isPartOf":{"@type":"WebSite","name":"Tư vấn Internet FPT","url":SITE_ORIGIN + "/"},"about":[{"@type":"Thing","name":"Internet FPT"},{"@type":"AdministrativeArea","name":p["name"]}]}
    breadcrumb_json = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Trang chủ","item":SITE_ORIGIN + "/"},{"@type":"ListItem","position":2,"name":"Khu vực","item":SITE_ORIGIN + "/khu-vuc/"},{"@type":"ListItem","position":3,"name":p["name"],"item":url}]}
    alias_html = alias_section(p)
    faq_html = "".join(f'<details{" open" if i == 0 else ""}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for i,(q,a) in enumerate(faqs))
    return f'''<!DOCTYPE html>
<html lang="vi"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc, quote=True)}"/>
<meta name="keywords" content="{escape(", ".join(core_keywords), quote=True)}"/>
<meta name="robots" content="index,follow,max-image-preview:large"/>
<link rel="canonical" href="{url}"/>
<meta property="og:title" content="{escape(title, quote=True)}"/>
<meta property="og:description" content="{escape(desc, quote=True)}"/>
<meta property="og:type" content="website"/><meta property="og:url" content="{url}"/>
<meta property="og:image" content="{SITE_ORIGIN}/assets/images/seo/khu-vuc-hero.webp"/>
<link rel="stylesheet" href="/fpt/assets/css/styles.css"/>
<script type="application/ld+json">{json.dumps(webpage_json, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_json, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(breadcrumb_json, ensure_ascii=False)}</script>
</head>
<body data-local-page="{escape(slug)}">{nav_html()}<main>
<section class="seo-hero"><img alt="Minh họa kiểm tra Internet FPT tại {name}" decoding="async" fetchpriority="high" height="900" loading="eager" src="/fpt/assets/images/seo/khu-vuc-hero.webp" width="1600"/><div class="container inner"><div class="breadcrumbs"><a href="/fpt/">Trang chủ</a><span>›</span><a href="/fpt/khu-vuc/">Khu vực</a><span>›</span><span>{name}</span></div><span class="eyebrow">Kiểm tra theo địa chỉ • Mã tỉnh {escape(p["code"])}</span><h1>Lắp mạng FPT tại {name}</h1><p>Tra cứu theo tỉnh/thành hiện hành, đối chiếu nhu cầu Internet, WiFi, Camera và combo trước khi gửi yêu cầu kiểm tra hạ tầng tại địa chỉ cụ thể.</p><div class="chips"><span class="chip">Internet FPT {name}</span><span class="chip">WiFi FPT {name}</span><span class="chip">Kiểm tra hạ tầng</span></div><div class="cta-row"><a class="btn btn-primary" href="/fpt/lien-he/">Kiểm tra & đăng ký</a><a class="btn btn-secondary" href="/fpt/goi-cuoc-fpt/">Xem gói cước</a></div></div></section>
<section class="section"><div class="container seo-grid"><article class="content-card"><div class="hold-local"><strong>Nguyên tắc dữ liệu địa phương:</strong> Trang này chỉ dùng dữ liệu hành chính đã xác minh để định tuyến tìm kiếm. Không suy diễn rằng toàn bộ {name} có cùng hạ tầng, giá, khuyến mãi hoặc thời gian lắp đặt. Các thông tin đó phải kiểm tra theo địa chỉ.</div>
<h2>{escape(intro_h2)}</h2><p>{escape(intro_text)}</p><p>Với nhu cầu lắp mạng FPT tại {name}, cách an toàn là tách quyết định thành ba lớp: <strong>địa chỉ có khả năng triển khai hay không</strong>, <strong>gói nào phù hợp số người và thiết bị</strong>, và <strong>WiFi trong nhà có cần mở rộng vùng phủ hay không</strong>. Cách này tránh chọn gói chỉ vì tên gọi hoặc một con số tốc độ.</p>
<h2>{name} trong danh mục 34 tỉnh/thành hiện hành</h2><p>{admin_copy(p)}</p>{alias_html}<p><a href="{admin_source}" rel="nofollow">Nguồn danh mục 34 đơn vị hành chính cấp tỉnh</a> · <a href="{code_source}" rel="nofollow">Nguồn mã đơn vị hành chính</a>. Dữ liệu hành chính được đối chiếu ngày 17/08/2026.</p>
<img alt="Minh họa cách chọn Internet và WiFi theo nhu cầu tại {name}" class="seo-image" decoding="async" height="675" loading="lazy" src="/fpt/assets/images/seo/khu-vuc-body.webp" width="1200"/>
<h2>Checklist trước khi đăng ký tại {name}</h2><ul><li><strong>Địa chỉ:</strong> cung cấp khu vực lắp đặt đủ để kiểm tra khả năng triển khai; không cần gửi thông tin nhạy cảm trong bước tư vấn ban đầu.</li><li><strong>Số thiết bị:</strong> tính cả điện thoại, TV, laptop, camera, máy chơi game và thiết bị thông minh hoạt động đồng thời.</li><li><strong>Không gian:</strong> ghi nhận diện tích, số tầng, tường/vật cản và nơi dự kiến đặt modem để đánh giá vùng phủ WiFi.</li><li><strong>Nhu cầu:</strong> phân biệt xem phim/học tập với game, livestream, camera cloud, làm việc từ xa hoặc tải dữ liệu lớn.</li><li><strong>Đi dây:</strong> với TV, PC game, camera hoặc thiết bị cố định, nên cân nhắc Ethernet để giảm phụ thuộc vào sóng WiFi.</li><li><strong>Xác minh cuối:</strong> hỏi lại giá, ưu đãi, thiết bị, phí phát sinh và thời gian lắp ở đúng địa chỉ trước khi chốt.</li></ul>
<h2>Chọn nhóm dịch vụ theo nhu cầu</h2><div class="link-grid"><a class="link-tile" href="/fpt/goi-cuoc-fpt/"><strong>Gói cước Internet</strong><span>So sánh theo nhu cầu và thiết bị</span></a><a class="link-tile" href="/fpt/wifi-6-fpt/"><strong>WiFi 6 FPT</strong><span>Thiết bị phổ biến, cân bằng chi phí</span></a><a class="link-tile" href="/fpt/wifi-7/"><strong>WiFi 7</strong><span>Tìm hiểu khi có thiết bị tương thích</span></a><a class="link-tile" href="/fpt/mesh-wifi-fpt/"><strong>Mesh WiFi</strong><span>Mở rộng vùng phủ nhà nhiều phòng/tầng</span></a><a class="link-tile" href="/fpt/camera-fpt/"><strong>Camera FPT</strong><span>Đánh giá upload và vị trí camera</span></a><a class="link-tile" href="/fpt/internet-truyen-hinh-fpt/"><strong>Internet + truyền hình</strong><span>Kiểm tra combo theo nhu cầu giải trí</span></a></div>
<h2>Không nên hiểu “giá FPT {name}” theo một con số cố định</h2><p>Cụm từ tìm kiếm về bảng giá, khuyến mãi hoặc phí lắp đặt thường có ý định thương mại cao, nhưng nội dung dễ lỗi thời. Trang này không gắn một mức giá local cố định. Thay vào đó, hãy dùng <a href="/fpt/bang-gia-fpt/">bảng giá tham khảo</a> để hiểu cấu trúc gói, sau đó xác minh lại giá và điều kiện tại địa chỉ ở {name} trước khi đăng ký.</p>
<h2>Nếu WiFi yếu dù tốc độ đường truyền cao</h2><p>Vấn đề có thể nằm ở vị trí modem, khoảng cách, vật cản, nhiễu sóng hoặc số thiết bị cùng lúc. Với nhà dài hoặc nhiều tầng, nên khảo sát vị trí điểm phát và cân nhắc <a href="/fpt/mesh-wifi-fpt/">Mesh WiFi</a>. Nếu cần độ ổn định cao cho PC game, TV hoặc camera, kết nối có dây vẫn là lựa chọn đáng cân nhắc.</p>
<h2>Cách xử lý các truy vấn theo tên tỉnh/thành cũ</h2><p>Sau thay đổi đơn vị hành chính, người dùng vẫn có thể tìm bằng tên cũ. Hệ thống keyword của website giữ các truy vấn đó nhưng chỉ định <strong>một URL owner hiện hành</strong> là <code>/khu-vuc/{escape(slug)}/</code>. Cách này giúp người đọc đến đúng ngữ cảnh hiện tại mà không tạo hàng loạt trang đổi tên địa phương giống nhau.</p>
<h2>Câu hỏi thường gặp về FPT tại {name}</h2><div class="faq">{faq_html}</div></article><aside><div class="content-card toc"><span class="eyebrow">Đi tiếp theo nhu cầu</span><h2 style="font-size:26px">Kiểm tra trước khi chốt</h2><div class="link-grid" style="grid-template-columns:1fr"><a class="link-tile" href="/fpt/lien-he/"><strong>Kiểm tra theo địa chỉ</strong><span>Gửi nhu cầu và khu vực lắp đặt</span></a><a class="link-tile" href="/fpt/goi-cuoc-fpt/"><strong>Gói cước FPT</strong><span>So sánh nhóm gói hiện có trên website</span></a><a class="link-tile" href="/fpt/giai-phap/nha-nhieu-tang/"><strong>Nhà nhiều tầng</strong><span>WiFi, Mesh và vị trí điểm phát</span></a><a class="link-tile" href="/fpt/ho-tro/"><strong>Hỗ trợ</strong><span>Xử lý các vấn đề mạng thường gặp</span></a></div><div class="fact-card" style="margin-top:16px"><strong>Phạm vi bằng chứng</strong><p>Đã xác minh: tên/mã đơn vị hành chính cấp tỉnh. Chưa mặc định: hạ tầng, giá, khuyến mãi, thiết bị hoặc SLA tại từng địa chỉ.</p></div></div></aside></div></section></main>{footer_html()}<script src="/fpt/assets/js/main.js"></script></body></html>'''


def render_index(data: dict) -> str:
    cards = []
    for p in data["provinces"]:
        old = [x for x in p["merged_from"] if x != p["name"]]
        note = f'Tên cũ liên quan: {", ".join(old)}' if old else "Tên tỉnh/thành hiện hành được giữ nguyên"
        cards.append(f'<a class="link-tile" href="/fpt/khu-vuc/{escape(p["slug"])}/"><strong>{escape(p["name"])}</strong><span>Mã {escape(p["code"])} · {escape(note)}</span></a>')
    cards_html = "".join(cards)
    desc = "Danh mục 34 tỉnh/thành hiện hành để tra cứu lắp mạng FPT theo địa chỉ. Mỗi trang local có canonical riêng và không mặc định giá/hạ tầng khi chưa xác minh."
    webpage = {"@context":"https://schema.org","@type":"CollectionPage","name":"Lắp mạng FPT theo 34 tỉnh/thành","description":desc,"url":SITE_ORIGIN + "/khu-vuc/","inLanguage":"vi-VN","dateModified":UPDATED}
    return f'''<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>Lắp mạng FPT theo 34 tỉnh/thành | Kiểm tra theo địa chỉ</title><meta name="description" content="{escape(desc, quote=True)}"/><meta name="robots" content="index,follow,max-image-preview:large"/><link rel="canonical" href="{SITE_ORIGIN}/khu-vuc/"/><meta property="og:title" content="Lắp mạng FPT theo 34 tỉnh/thành"/><meta property="og:description" content="{escape(desc, quote=True)}"/><meta property="og:type" content="website"/><meta property="og:url" content="{SITE_ORIGIN}/khu-vuc/"/><meta property="og:image" content="{SITE_ORIGIN}/assets/images/seo/khu-vuc-hero.webp"/><link rel="stylesheet" href="/fpt/assets/css/styles.css"/><script type="application/ld+json">{json.dumps(webpage,ensure_ascii=False)}</script></head><body data-local-index="true">{nav_html()}<main><section class="seo-hero"><img alt="Lắp mạng FPT theo 34 tỉnh/thành" decoding="async" fetchpriority="high" height="900" loading="eager" src="/fpt/assets/images/seo/khu-vuc-hero.webp" width="1600"/><div class="container inner"><div class="breadcrumbs"><a href="/fpt/">Trang chủ</a><span>›</span><span>Khu vực</span></div><span class="eyebrow">34 tỉnh/thành hiện hành</span><h1>Lắp mạng FPT theo tỉnh/thành</h1><p>Chọn tỉnh/thành hiện hành để kiểm tra nhu cầu, hạ tầng theo địa chỉ và các nhóm dịch vụ Internet, WiFi, Camera, combo phù hợp.</p><div class="cta-row"><a class="btn btn-primary" href="/fpt/lien-he/">Kiểm tra theo địa chỉ</a><a class="btn btn-secondary" href="/fpt/goi-cuoc-fpt/">Xem gói cước</a></div></div></section><section class="section"><div class="container"><article class="content-card"><div class="hold-local"><strong>Phạm vi local:</strong> Website có 34 URL tỉnh/thành hiện hành. Tên tỉnh/thành trước sắp xếp được map về URL hiện hành tương ứng; không tạo doorway page theo tên cũ. Khả năng lắp đặt, giá và ưu đãi vẫn phải xác minh theo địa chỉ.</div><h2>Chọn tỉnh/thành</h2><p>Danh mục dùng cấu trúc 34 đơn vị hành chính cấp tỉnh hiện hành. Mỗi URL là owner cho một tỉnh/thành và nhóm tên địa phương cũ liên quan.</p><div class="link-grid">{cards_html}</div><h2>Cách dùng trang khu vực</h2><ol><li>Chọn tỉnh/thành hiện hành.</li><li>Đọc phần tên địa phương trước sắp xếp nếu bạn đang tìm theo tên cũ.</li><li>Xác định nhu cầu Internet/WiFi/Camera và số thiết bị.</li><li>Gửi địa chỉ để kiểm tra khả năng triển khai trước khi chốt giá hoặc ưu đãi.</li></ol><p>Nguồn hành chính: <a href="{escape(data["admin_source"],quote=True)}" rel="nofollow">Danh sách 34 tỉnh/thành</a> và <a href="{escape(data["code_source"],quote=True)}" rel="nofollow">danh mục mã đơn vị hành chính</a>.</p></article></div></section></main>{footer_html()}<script src="/fpt/assets/js/main.js"></script></body></html>'''


def update_sitemap(site: Path, provinces: list[dict]) -> None:
    path = site / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'<url><loc>https://[^<]+/khu-vuc/[^<]+/</loc><lastmod>[^<]+</lastmod></url>\s*', '', text)
    local_rows = "\n".join(f"<url><loc>{SITE_ORIGIN}/khu-vuc/{escape(p['slug'])}/</loc><lastmod>{UPDATED}</lastmod></url>" for p in provinces)
    text = text.replace("</urlset>", local_rows + "\n</urlset>")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--site", required=True); args = parser.parse_args()
    site = Path(args.site); root = Path(__file__).resolve().parents[1]; data = load_provinces(root); provinces = data["provinces"]
    if len(provinces) != 34: raise SystemExit(f"Expected 34 provinces/cities, got {len(provinces)}")
    (site / "khu-vuc").mkdir(parents=True, exist_ok=True)
    (site / "khu-vuc" / "index.html").write_text(render_index(data), encoding="utf-8")
    for p in provinces:
        out = site / "khu-vuc" / p["slug"] / "index.html"; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(render_page(p, data), encoding="utf-8")
    update_sitemap(site, provinces)
    print(f"LOCAL PAGES GENERATED: {len(provinces)} detail pages + local index; sitemap updated")


if __name__ == "__main__": main()
