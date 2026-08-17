from __future__ import annotations

import argparse
import re
from html import escape
from pathlib import Path

OBSERVED_AT = "2026-08-18"

INTERNET = [
    {"id":"giga","type":"internet","name":"Internet GIGA","url":"goi-cuoc/giga/","price":"195.000đ/tháng","speed":"300 / 300 Mbps","device":"Modem Wi-Fi 6","fit":"Gia đình, học tập, xem phim, làm việc","badge":"Giá tốt","features":["Băng thông đối xứng 300 Mbps","Wi-Fi 6 băng tần kép","Hỗ trợ kỹ thuật 24/7"]},
    {"id":"sky","type":"internet","name":"Internet SKY","url":"goi-cuoc/sky/","price":"195.000đ/tháng","speed":"1 Gbps / 300 Mbps","device":"Modem Wi-Fi 6","fit":"Gia đình nhiều thiết bị, 4K, gaming","badge":"Phổ biến","features":["Download đến 1 Gbps","Wi-Fi 6 băng tần kép","Phù hợp nhiều thiết bị đồng thời"]},
    {"id":"meta","type":"internet","name":"Internet META","url":"goi-cuoc/meta/","price":"295.000đ/tháng","speed":"1 Gbps / 1 Gbps","device":"Modem Wi-Fi 6","fit":"Upload cao, cloud, creator, gia đình lớn","badge":"Đối xứng","features":["1 Gbps download và upload","Kết nối đến 25 thiết bị theo nguồn FPT","Phù hợp nhu cầu upload cao"]},
    {"id":"f-game","type":"internet","name":"Internet F-Game","url":"goi-cuoc/f-game/","price":"225.000đ/tháng","speed":"1 Gbps / 300 Mbps","device":"Modem Wi-Fi 6 + Ultra Fast","fit":"Game thủ, streamer","badge":"Gaming","features":["Ultra Fast hỗ trợ 50+ tựa game","Giảm độ trễ tới 16 ms theo nguồn FPT","Ưu tiên trải nghiệm chơi game online"]},
    {"id":"speedx2","type":"internet","name":"FPT SpeedX2","url":"goi-cuoc/speedx2/","price":"999.000đ/tháng","speed":"2 Gbps / 2 Gbps","device":"Wi-Fi 7 · XGS-PON","fit":"Nhà lớn, workstation, tải cao","badge":"Wi-Fi 7","features":["Băng thông đối xứng 2 Gbps","Hạ tầng XGS-PON","Khả năng chịu tải cao"]},
    {"id":"speedx2-pro","type":"internet","name":"FPT SpeedX2 Pro","url":"goi-cuoc/speedx2-pro/","price":"1.099.000đ/tháng","speed":"2 Gbps / 2 Gbps","device":"Modem + Mesh Wi-Fi 7","fit":"Gia đình lớn, doanh nghiệp nhỏ, AR/VR","badge":"Pro","features":["Wi-Fi 7 ba băng tần","Hỗ trợ gần 100 thiết bị theo nguồn FPT","Tích hợp FPT Play VIP và Box650"]},
    {"id":"speedx10","type":"internet","name":"FPT SpeedX10","url":"goi-cuoc/speedx10/","price":"1.599.000đ/tháng","speed":"10 Gbps / 10 Gbps","device":"Wi-Fi 7 · XGS-PON","fit":"Studio, creator, smart home tải cực cao","badge":"10G","features":["Băng thông đối xứng 10 Gbps","XGS-PON + Wi-Fi 7","Dành cho tác vụ và tải đồng thời rất cao"]},
    {"id":"speedx10-pro","type":"internet","name":"FPT SpeedX10 Pro","url":"goi-cuoc/speedx10-pro/","price":"1.690.000đ/tháng","speed":"10 Gbps / 10 Gbps","device":"Modem + Mesh Wi-Fi 7","fit":"Studio lớn, văn phòng, livestream 8K, AR/VR","badge":"Cao cấp","features":["Wi-Fi 7 cao cấp, gần 100 thiết bị","Băng thông 10 Gbps đối xứng","Tích hợp FPT Play VIP và Box650"]},
]

PLAY = [
    {"id":"combo-giga","type":"play","name":"Combo GIGA + FPT Play","url":"goi-cuoc/combo-giga/","price":"200.000đ/tháng","speed":"300 / 300 Mbps","device":"Wi-Fi 6 + FPT Play Box","fit":"Gia đình cần Internet + truyền hình","badge":"Combo","features":["Internet GIGA","FPT Play Box","Hơn 130 kênh theo trang FPT lắp Wi-Fi"]},
    {"id":"combo-sky","type":"play","name":"Combo SKY + FPT Play","url":"goi-cuoc/combo-sky/","price":"209.000đ/tháng","speed":"1 Gbps / 300 Mbps","device":"Wi-Fi 6 + FPT Play Box","fit":"Nhà nhiều thiết bị + giải trí","badge":"Combo","features":["Internet SKY","FPT Play Box","Hơn 130 kênh theo trang FPT lắp Wi-Fi"]},
    {"id":"combo-meta","type":"play","name":"Combo META + FPT Play","url":"goi-cuoc/combo-meta/","price":"320.000đ/tháng","speed":"1 Gbps / 1 Gbps","device":"Wi-Fi 6 + FPT Play Box","fit":"Upload cao + truyền hình","badge":"Đối xứng","features":["Internet META đối xứng","FPT Play Box","Nội dung truyền hình và thể thao"]},
    {"id":"combo-f-game","type":"play","name":"Combo F-Game + FPT Play","url":"goi-cuoc/combo-f-game/","price":"270.000đ/tháng","speed":"1 Gbps / 300 Mbps","device":"Wi-Fi 6 + Play Box + Ultra Fast","fit":"Game + phim + truyền hình","badge":"Gaming Combo","features":["Ultra Fast hỗ trợ 50+ game","FPT Play Box","Kho phim 4K và truyền hình"]},
    {"id":"fpt-play","type":"play","name":"FPT Play","url":"fpt-play/","price":"Kiểm tra gói nội dung","speed":"Dịch vụ truyền hình / OTT","device":"FPT Play Box tùy gói","fit":"Phim, truyền hình, thể thao","badge":"Giải trí","features":["Kho nội dung FPT Play","Có gói tích hợp cùng Internet","Thiết bị và quyền lợi tùy gói"]},
    {"id":"sports-sky","type":"play-extra","name":"Combo Thể Thao SKY","url":"fpt-play/","price":"269.000đ/tháng","speed":"1 Gbps / 300 Mbps","device":"Wi-Fi 6 + FPT Play Box","fit":"Internet + thể thao cao cấp","badge":"Thể thao","features":["Internet SKY","FPT Play Box","Nội dung thể thao theo gói hiện hành"]},
    {"id":"sports-meta","type":"play-extra","name":"Combo Thể Thao META","url":"fpt-play/","price":"369.000đ/tháng","speed":"1 Gbps / 1 Gbps","device":"Wi-Fi 6 + FPT Play Box","fit":"Upload cao + thể thao","badge":"Thể thao","features":["Internet META đối xứng","FPT Play Box","Nội dung thể thao theo gói hiện hành"]},
]

CAMERA = [
    {"id":"camera-fpt","type":"camera","name":"Camera FPT","url":"camera-fpt/","price":"Từ 510.000đ","speed":"Thiết bị Camera AI","device":"Play 4 / IQ 4S và các combo","fit":"Tổng quan camera trong/ngoài nhà","badge":"Camera AI","features":["Quản lý trên hệ sinh thái FPT","Có lựa chọn mua lẻ và combo","Cloud tùy gói dịch vụ"]},
    {"id":"play3","type":"camera","name":"Camera Play 3","url":"camera-fpt/play-3/","price":"Kiểm tra theo thời điểm","speed":"Camera trong nhà","device":"Camera Play 3","fit":"Quan sát trong nhà","badge":"Trong nhà","features":["Trang sản phẩm hiện có trên website","Giá cần kiểm tra lại theo thời điểm","Có thể kết hợp dịch vụ Cloud"]},
    {"id":"play4","type":"camera","name":"Camera Play 4","url":"camera-fpt/play-4/","price":"Từ 510.000đ","speed":"Camera AI","device":"Camera Play 4","fit":"Giám sát nhà ở","badge":"Mới","features":["Sản phẩm Camera AI FPT","Có các gói Internet + Camera","Cloud tùy cấu hình dịch vụ"]},
    {"id":"iq4s","type":"camera-extra","name":"Camera IQ 4S","url":"camera-fpt/","price":"Từ 510.000đ","speed":"Camera AI","device":"Camera IQ 4S","fit":"Giám sát trong nhà / gia đình","badge":"AI","features":["Sản phẩm Camera AI FPT","Có lựa chọn mua cùng Internet","Cloud tùy gói"]},
    {"id":"camera-2","type":"camera-extra","name":"Combo 2 Camera","url":"camera-fpt/","price":"Từ 950.000đ","speed":"2 camera","device":"Trong nhà / ngoài trời tùy combo","fit":"Nhà nhỏ, cửa hàng nhỏ","badge":"2 Camera","features":["Có cấu hình 2 trong nhà","Có cấu hình 2 ngoài trời","Có cấu hình trong + ngoài"]},
    {"id":"camera-3","type":"camera-extra","name":"Combo 3 Camera","url":"camera-fpt/","price":"Từ 1.150.000đ","speed":"3 camera","device":"Nhiều cấu hình trong / ngoài nhà","fit":"Nhà nhiều khu vực, cửa hàng","badge":"3 Camera","features":["Có nhiều tổ hợp trong/ngoài nhà","Quản lý tập trung","Cloud tùy gói"]},
    {"id":"camera-5","type":"camera-extra","name":"Combo 5 Camera","url":"camera-fpt/","price":"Từ 2.100.000đ","speed":"5 camera","device":"Tổ hợp trong + ngoài nhà","fit":"Nhà lớn, cửa hàng, cơ sở kinh doanh","badge":"5 Camera","features":["Phủ nhiều vị trí quan sát","Quản lý tập trung","Cloud tùy gói"]},
]

CAMERA_BUNDLES = [
    {"id":"gigaeyes-play4","type":"camera-bundle","name":"GigaEyes3 Play4","url":"camera-fpt/","price":"220.000đ/tháng","speed":"300 / 300 Mbps","device":"Wi-Fi 6 + Camera Play 4","fit":"Internet GIGA + camera","badge":"Internet + Camera","features":["Camera Play 4","Cloud 3 ngày","Dòng combo cho 2–5 camera theo nguồn FPT"]},
    {"id":"skyeyes-play4","type":"camera-bundle","name":"SkyEyes3 Play4","url":"camera-fpt/","price":"245.000đ/tháng","speed":"1 Gbps / 300 Mbps","device":"Wi-Fi 6 + Camera Play 4","fit":"Internet SKY + camera","badge":"Internet + Camera","features":["Camera Play 4","Cloud 3 ngày","Dòng combo cho 2–5 camera theo nguồn FPT"]},
    {"id":"triple-gigaeyes","type":"camera-bundle","name":"Triple GigaEyes3 Play4 + FPT Play","url":"camera-fpt/","price":"270.000đ/tháng","speed":"300 / 300 Mbps","device":"Wi-Fi 6 + Play Box + Camera Play 4","fit":"Internet + truyền hình + camera","badge":"3 trong 1","features":["FPT Play Box","Camera Play 4","Cloud 3 ngày"]},
    {"id":"triple-skyeyes","type":"camera-bundle","name":"Triple SkyEyes3 Play4 + FPT Play","url":"camera-fpt/","price":"270.000đ/tháng","speed":"1 Gbps / 300 Mbps","device":"Wi-Fi 6 + Play Box + Camera Play 4","fit":"Internet tốc độ cao + TV + camera","badge":"3 trong 1","features":["Internet SKY","FPT Play Box","Camera Play 4 + Cloud 3 ngày"]},
]

SOURCES = [
    ("Internet & Combo", "https://fpt.vn/lap-wifi"),
    ("F-Game / META", "https://fpt.vn/internet/game-thu"),
    ("SpeedX2 Pro", "https://fpt.vn/internet/speed-x2-pro"),
    ("SpeedX10 Pro", "https://fpt.vn/internet/speed-x10-pro"),
    ("Camera", "https://fpt.vn/camera"),
]


def product_card(item: dict, location: str) -> str:
    features = "".join(f"<li>{escape(x)}</li>" for x in item["features"])
    detail_href = "../../" + item["url"]
    return f'''<article class="local-plan-card" data-local-plan-card data-local-product="{escape(item['type'])}" data-plan-id="{escape(item['id'])}">
<div class="local-plan-top"><span class="local-plan-badge">{escape(item['badge'])}</span><h3>{escape(item['name'])}</h3><p class="local-plan-price"><small>Chỉ từ / tham khảo</small><strong>{escape(item['price'])}</strong></p></div>
<div class="local-plan-specs"><div><span>Tốc độ / loại</span><strong>{escape(item['speed'])}</strong></div><div><span>Thiết bị</span><strong>{escape(item['device'])}</strong></div></div>
<p class="local-plan-fit"><strong>Phù hợp:</strong> {escape(item['fit'])}</p><ul class="local-plan-features">{features}</ul>
<div class="local-plan-actions"><a class="btn btn-secondary" href="{detail_href}">Xem chi tiết</a><a class="btn btn-primary" href="#dang-ky" data-select-local-plan="{escape(item['name'])}">Kiểm tra tại {escape(location)}</a></div>
</article>'''


def group(title: str, subtitle: str, items: list[dict], location: str) -> str:
    return f'''<div class="local-plan-group"><div class="local-plan-group-head"><h3>{escape(title)}</h3><p>{escape(subtitle)}</p></div><div class="local-plan-grid">{''.join(product_card(x, location) for x in items)}</div></div>'''


def catalog_section(location: str) -> str:
    source_links = " · ".join(f'<a href="{url}" rel="nofollow noopener" target="_blank">{escape(label)}</a>' for label, url in SOURCES)
    return f'''<section class="section local-commerce" id="goi-dich-vu-dia-phuong" data-catalog-observed="{OBSERVED_AT}"><div class="container">
<div class="section-head"><span class="eyebrow">Gói cước FPT tại {escape(location)}</span><h2>Chọn trực tiếp gói Internet, FPT Play và Camera</h2><p>Không còn chỉ là danh sách đường dẫn. Dưới đây là catalog sản phẩm có tốc độ, thiết bị, mức giá tham khảo và nút đăng ký ngay trên trang {escape(location)}.</p></div>
<div class="local-price-notice"><strong>Lưu ý về giá tại {escape(location)}:</strong> Các mức “chỉ từ” dưới đây được đối chiếu từ website FPT Telecom ngày {OBSERVED_AT}. FPT nêu rõ giá, thiết bị và ưu đãi có thể thay đổi theo khu vực và thời điểm; báo giá cuối cùng chỉ được xác nhận sau khi kiểm tra địa chỉ.</div>
<nav class="local-catalog-jump" aria-label="Nhóm gói cước"><a href="#local-internet">Internet</a><a href="#local-play">Internet + FPT Play</a><a href="#local-camera">Camera</a><a href="#local-camera-bundle">Internet + Camera</a></nav>
<div id="local-internet">{group('8 gói Internet FPT', 'Từ nhu cầu gia đình đến Wi-Fi 7 XGS-PON 10 Gbps.', INTERNET, location)}</div>
<div id="local-play">{group('Internet + truyền hình FPT Play', 'Combo phổ thông, gaming và nhóm thể thao hiện hành.', PLAY, location)}</div>
<div id="local-camera">{group('Camera FPT', 'Camera mua lẻ và combo nhiều camera cho nhà ở/cửa hàng.', CAMERA, location)}</div>
<div id="local-camera-bundle">{group('Combo Internet + Camera', 'Gói tích hợp đường truyền, camera và tùy cấu hình có FPT Play.', CAMERA_BUNDLES, location)}</div>
<div class="local-catalog-source"><strong>Nguồn sản phẩm:</strong> {source_links}<p>Ngày đối chiếu: {OBSERVED_AT}. Không dùng mức giá tham khảo này để cam kết một giá duy nhất cho toàn {escape(location)}.</p></div>
<div class="cta-row local-catalog-bottom"><a class="btn btn-primary" href="#dang-ky">Gửi địa chỉ để chốt gói</a><a class="btn btn-secondary" data-local-news-link href="tin-tuc/">Tin tức {escape(location)}</a></div>
</div></section>'''


def location_name(html: str, path: Path) -> str:
    match = re.search(r"<h1[^>]*>\s*Lắp mạng FPT tại\s+(.*?)</h1>", html, flags=re.I | re.S)
    if not match:
        raise SystemExit(f"LOCAL COMMERCE BUILD FAIL: cannot read location from {path}")
    return re.sub(r"<[^>]+>", "", match.group(1)).strip()


def upgrade(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    location = location_name(html, path)
    pattern = re.compile(r'<section class="section" id="goi-dich-vu-dia-phuong">.*?</section>', flags=re.I | re.S)
    if not pattern.search(html):
        raise SystemExit(f"LOCAL COMMERCE BUILD FAIL: simple catalog missing in {path}")
    html = pattern.sub(catalog_section(location), html, count=1)
    css = '<link rel="stylesheet" href="../../assets/css/local-catalog.css" data-local-catalog-style="v1"/>'
    if 'data-local-catalog-style=' not in html:
        if '</head>' not in html:
            raise SystemExit(f"LOCAL COMMERCE BUILD FAIL: </head> missing in {path}")
        html = html.replace('</head>', css + '</head>', 1)
    path.write_text(html, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    root = Path(args.site) / 'khu-vuc'
    pages = sorted(root.glob('*/index.html'))
    if len(pages) != 34:
        raise SystemExit(f"LOCAL COMMERCE BUILD FAIL: expected 34 province pages, got {len(pages)}")
    for page in pages:
        upgrade(page)
    print('Local commerce upgraded: 34/34 province pages, 26 product cards each (8 Internet + 7 FPT Play/combo + 7 Camera + 4 Internet/Camera)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
