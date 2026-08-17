from __future__ import annotations

import argparse
import re
from html import escape, unescape
from pathlib import Path

OBSERVED_AT = "2026-08-18"
EXPECTED_BASE = 56

INTERNET = "https://fpt.vn/internet"
FAMILY = "https://fpt.vn/internet/gia-dinh"
PLAY = "https://fpt.vn/truyen-hinh-fpt-play"
BUSINESS = "https://fpt.vn/internet/doanh-nghiep"
CAMERA = "https://fpt.vn/camera"


def offer(pid, group, name, price, down, up, device, fit, benefits, source):
    return {
        "id": pid, "group": group, "name": name, "price": price, "down": down, "up": up,
        "device": device, "fit": fit, "benefits": benefits, "source": source,
    }


OFFERS = [
    # FPT Play / V.VIP / standalone entertainment.
    offer("combo-giga-vvip", "official-play", "Combo Giga - V.VIP", "220.000đ/tháng", "300 Mbps", "300 Mbps", "Modem Wi‑Fi 6 + FPT Play", "Gia đình cần Internet và bóng đá/giải trí", ["Xem Ngoại hạng Anh theo quyền lợi V.VIP", "120 kênh truyền hình theo catalog hiện hành", "Dùng Internet và giải trí trong một combo"], PLAY),
    offer("combo-sky-vvip", "official-play", "Combo Sky - V.VIP", "239.000đ/tháng", "1 Gbps", "300 Mbps", "Modem Wi‑Fi 6 + FPT Play", "Nhà nhiều thiết bị, xem thể thao", ["Internet SKY tốc độ cao", "Quyền lợi V.VIP", "120 kênh truyền hình theo catalog hiện hành"], PLAY),
    offer("combo-meta-vvip", "official-play", "Combo Meta - V.VIP", "339.000đ/tháng", "1 Gbps", "1 Gbps", "Modem Wi‑Fi 6 + FPT Play", "Upload cao kết hợp giải trí", ["Băng thông đối xứng", "Quyền lợi V.VIP", "Phù hợp vừa làm việc vừa xem thể thao"], PLAY),
    offer("combo-lux500-vvip", "official-play", "Combo Lux500 - V.VIP", "830.000đ/tháng", "500 Mbps", "500 Mbps", "Wi‑Fi 6 + Access Point + FPT Play", "Nhóm người dùng tải cao, nhiều thiết bị", ["Kết nối nhiều thiết bị", "Tích hợp Ultra Fast", "FPT Play/V.VIP trong cùng gói"], PLAY),
    offer("combo-lux800-vvip", "official-play", "Combo Lux800 - V.VIP", "1.030.000đ/tháng", "800 Mbps", "800 Mbps", "Wi‑Fi 6 + Access Point + FPT Play", "Nhà/văn phòng nhiều thiết bị", ["Băng thông 800 Mbps đối xứng", "Tích hợp Ultra Fast", "FPT Play/V.VIP"], PLAY),
    offer("combo-speedx2-vvip", "official-play", "Combo SpeedX2 - V.VIP", "1.029.000đ/tháng", "2 Gbps", "2 Gbps", "Wi‑Fi 7 + XGS-PON + FPT Play", "Gia đình cao cấp cần Wi‑Fi 7 và thể thao", ["2 Gbps đối xứng", "Wi‑Fi 7", "Quyền lợi V.VIP"], PLAY),
    offer("combo-speedx10-vvip", "official-play", "Combo SpeedX10 - V.VIP", "1.629.000đ/tháng", "10 Gbps", "10 Gbps", "Wi‑Fi 7 + XGS-PON + FPT Play", "Studio/nhà tải cực cao và giải trí", ["10 Gbps đối xứng", "Wi‑Fi 7", "Quyền lợi V.VIP"], PLAY),
    offer("vvip-1", "official-play", "Gói V.VIP 1", "120.000đ/tháng", "Dịch vụ FPT Play", "—", "TV / Box / Mobile / Web", "Người xem bóng đá và giải trí trên một luồng thể thao", ["Ngoại hạng Anh và FA Cup theo quyền lợi hiện hành", "Gần 100 kênh", "Hỗ trợ Full HD và nội dung 4K"], PLAY),
    offer("vvip-2", "official-play", "Gói V.VIP 2", "140.000đ/tháng", "Dịch vụ FPT Play", "—", "TV / Box / Mobile / Web", "Gia đình cần hai luồng thể thao đồng thời", ["Ngoại hạng Anh và FA Cup trên 2 thiết bị theo quyền lợi", "Gần 100 kênh", "Đa nền tảng"], PLAY),
    offer("fpt-play-cine", "official-play", "FPT Play Cine", "33.000đ/tháng", "Dịch vụ FPT Play", "—", "Smart TV / Mobile / Web", "Người ưu tiên phim bộ, thiếu nhi, anime", ["Kho phim bộ chọn lọc", "Nội dung thiếu nhi và anime", "Hỗ trợ 2 thiết bị xem đồng thời"], PLAY),
    offer("fpt-play-premium", "official-play", "FPT Play Premium", "75.000đ/tháng", "Dịch vụ FPT Play", "—", "Smart TV / Mobile / Web", "Gia đình cần truyền hình, phim và thể thao", ["Hơn 100 kênh", "Kho phim và thể thao", "Hỗ trợ 3 thiết bị xem đồng thời"], PLAY),
    offer("combo-an-tam", "official-play", "Combo An Tâm + FPT Play", "245.000đ/tháng", "300 Mbps", "300 Mbps", "Wi‑Fi 6 + FPT Play + F‑Safe", "Gia đình có trẻ em, cần Internet và bảo mật", ["Internet 300 Mbps đối xứng", "FPT Play", "Tích hợp F‑Safe"], PLAY),
    offer("combo-giai-tri", "official-play", "Combo Giải Trí", "200.000đ/tháng", "300 Mbps", "300 Mbps", "Wi‑Fi 6 + FPT Play", "Gia đình cần combo cơ bản", ["Internet 300 Mbps", "FPT Play", "Mức hiển thị cần xác nhận theo địa chỉ"], PLAY),

    # Business catalog.
    offer("lux500", "business", "Lux500", "800.000đ/tháng", "500 Mbps", "500 Mbps", "Wi‑Fi 6 + 1 Access Point", "Doanh nghiệp vừa, nhiều thiết bị", ["500 Mbps đối xứng", "Kết nối đến 125 thiết bị theo catalog", "Tích hợp Ultra Fast"], BUSINESS),
    offer("lux800", "business", "Lux800", "1.000.000đ/tháng", "800 Mbps", "800 Mbps", "Wi‑Fi 6 + 1 Access Point", "Doanh nghiệp nhiều thiết bị", ["800 Mbps đối xứng", "Kết nối đến 160 thiết bị theo catalog", "Tích hợp Ultra Fast"], BUSINESS),
    offer("combo-lux500", "business", "Combo Lux500", "875.600đ/tháng", "500 Mbps", "500 Mbps", "Wi‑Fi 6 + Access Point + FPT Play Box", "Doanh nghiệp cần Internet + truyền hình", ["500 Mbps đối xứng", "Ultra Fast", "FPT Play Box"], BUSINESS),
    offer("combo-lux800", "business", "Combo Lux800", "1.075.600đ/tháng", "800 Mbps", "800 Mbps", "Wi‑Fi 6 + Access Point + FPT Play Box", "Doanh nghiệp tải cao + truyền hình", ["800 Mbps đối xứng", "Ultra Fast", "FPT Play Box"], BUSINESS),
    offer("super300-biz", "business", "Super300 Biz", "450.000đ/tháng", "300 Mbps", "300 Mbps", "Cân bằng tải + 1 Access Point", "Cửa hàng/văn phòng cần thiết bị mạng doanh nghiệp", ["300 Mbps đối xứng", "Cân bằng tải", "1 Access Point"], BUSINESS),
    offer("super300-biz-plus", "business", "Super300 Biz Plus", "750.000đ/tháng", "300 Mbps", "300 Mbps", "Cân bằng tải + Access Point + IP tĩnh", "Doanh nghiệp cần IP tĩnh", ["300 Mbps đối xứng", "Cân bằng tải", "Tích hợp IP tĩnh"], BUSINESS),
    offer("super500-biz", "business", "Super500 Biz", "1.400.000đ/tháng", "500 Mbps", "500 Mbps", "Cân bằng tải + 1 Access Point", "Doanh nghiệp vừa mở rộng", ["500 Mbps đối xứng", "Cân bằng tải", "1 Access Point"], BUSINESS),
    offer("super500-biz-plus", "business", "Super500 Biz Plus", "1.700.000đ/tháng", "500 Mbps", "500 Mbps", "Cân bằng tải + Access Point + IP tĩnh", "Doanh nghiệp vừa cần IP tĩnh", ["500 Mbps đối xứng", "Cân bằng tải", "Tích hợp IP tĩnh"], BUSINESS),
    offer("super600-biz", "business", "Super600 Biz", "2.500.000đ/tháng", "600 Mbps", "600 Mbps", "Cân bằng tải + 1 Access Point", "Doanh nghiệp tải lớn", ["600 Mbps đối xứng", "Cân bằng tải", "1 Access Point"], BUSINESS),
    offer("super600-biz-plus", "business", "Super600 Biz Plus", "2.800.000đ/tháng", "600 Mbps", "600 Mbps", "Cân bằng tải + Access Point + IP tĩnh", "Doanh nghiệp tải lớn cần IP tĩnh", ["600 Mbps đối xứng", "Cân bằng tải", "Tích hợp IP tĩnh"], BUSINESS),
    offer("super800-biz", "business", "Super800 Biz", "3.400.000đ/tháng", "800 Mbps", "800 Mbps", "Cân bằng tải + 1 Access Point", "Doanh nghiệp nhiều người dùng", ["800 Mbps đối xứng", "Cân bằng tải", "1 Access Point"], BUSINESS),
    offer("super800-biz-plus", "business", "Super800 Biz Plus", "3.800.000đ/tháng", "800 Mbps", "800 Mbps", "Cân bằng tải + Access Point + IP tĩnh", "Doanh nghiệp nhiều người dùng cần IP tĩnh", ["800 Mbps đối xứng", "Cân bằng tải", "Tích hợp IP tĩnh"], BUSINESS),

    # Camera + Internet current nationwide-capable offers. Region-only Tây Nam Bộ F1/F2/F3 variants are deliberately excluded.
    offer("giga-antam7-play4-multi", "camera-current", "Giga An Tâm 7 - Play4 (từ 2 cam)", "220.000đ/tháng", "300 Mbps", "300 Mbps", "Wi‑Fi 6 + Camera Play4", "Gia đình cần Internet + nhiều camera trong nhà", ["Camera Play4", "Cloud An Tâm 7 ngày", "Có cấu hình từ 2 camera"], CAMERA),
    offer("giga-antam7-iq4s-multi", "camera-current", "Giga An Tâm 7 - IQ4S (từ 2 cam)", "220.000đ/tháng", "300 Mbps", "300 Mbps", "Wi‑Fi 6 + Camera IQ4S", "Gia đình cần Internet + camera ngoài trời", ["Camera IQ4S", "Cloud An Tâm 7 ngày", "Có cấu hình từ 2 camera"], CAMERA),
    offer("sky-antam7-play4-multi", "camera-current", "Sky An Tâm 7 - Play4 (từ 2 cam)", "245.000đ/tháng", "1 Gbps", "300 Mbps", "Wi‑Fi 6 + Camera Play4", "Nhà nhiều thiết bị + nhiều camera", ["Internet SKY", "Camera Play4", "Cloud An Tâm 7 ngày"], CAMERA),
    offer("sky-antam7-iq4s-multi", "camera-current", "Sky An Tâm 7 - IQ4S (từ 2 cam)", "245.000đ/tháng", "1 Gbps", "300 Mbps", "Wi‑Fi 6 + Camera IQ4S", "Nhà nhiều thiết bị + camera ngoài trời", ["Internet SKY", "Camera IQ4S", "Cloud An Tâm 7 ngày"], CAMERA),
    offer("sky-antam7-play4-one", "camera-current", "Sky An Tâm 7 - Play4 (1 cam)", "235.000đ/tháng", "1 Gbps", "300 Mbps", "Wi‑Fi 6 + 1 Camera Play4", "Gia đình cần một camera trong nhà", ["Camera Play4", "Cloud An Tâm 7 ngày", "Internet SKY"], CAMERA),
    offer("sky-antam7-iq4s-one", "camera-current", "Sky An Tâm 7 - IQ4S (1 cam)", "235.000đ/tháng", "1 Gbps", "300 Mbps", "Wi‑Fi 6 + 1 Camera IQ4S", "Gia đình cần một camera ngoài trời", ["Camera IQ4S", "Cloud An Tâm 7 ngày", "Internet SKY"], CAMERA),
    offer("triple-sky-antam7-play4", "camera-current", "Triple Sky An Tâm 7 - Play4 - FPT Play", "270.000đ/tháng", "1 Gbps", "300 Mbps", "Wi‑Fi 6 + FPT Play Box + Camera Play4", "Internet + giải trí + camera", ["FPT Play Box", "Camera Play4", "Cloud An Tâm 7 ngày"], CAMERA),

    # Wi-Fi 7 / XGS-PON + camera/entertainment variants.
    offer("speedx2-play4", "wifi7-current", "FPT SpeedX2 - Play4", "1.039.000đ/tháng", "2 Gbps", "2 Gbps", "Wi‑Fi 7 + Mesh + Camera Play4", "Nhà cao cấp cần 2 Gbps và camera trong nhà", ["XGS-PON 2 Gbps", "01 Mesh Wi‑Fi 7", "01 Camera Play4 + ZPlay"], FAMILY),
    offer("speedx2-iq4s", "wifi7-current", "FPT SpeedX2 - IQ4S", "1.039.000đ/tháng", "2 Gbps", "2 Gbps", "Wi‑Fi 7 + Mesh + Camera IQ4S", "Nhà cao cấp cần 2 Gbps và camera ngoài trời", ["XGS-PON 2 Gbps", "01 Mesh Wi‑Fi 7", "01 Camera IQ4S + ZPlay"], INTERNET),
    offer("speedx2-pro-play4", "wifi7-current", "FPT SpeedX2 Pro - Play4", "1.099.000đ/tháng", "2 Gbps", "2 Gbps", "Wi‑Fi 7 + Mesh + Play4 + FPT Play", "Nhà cao cấp cần camera + FPT Play", ["2 Gbps đối xứng", "Camera Play4", "FPT Play VIP & Box650"], INTERNET),
    offer("speedx2-pro-iq4s", "wifi7-current", "FPT SpeedX2 Pro - IQ4S", "1.099.000đ/tháng", "2 Gbps", "2 Gbps", "Wi‑Fi 7 + Mesh + IQ4S + FPT Play", "Nhà cao cấp cần camera ngoài trời + FPT Play", ["2 Gbps đối xứng", "Camera IQ4S", "FPT Play VIP & Box650"], INTERNET),
    offer("speedx2-eyes3-iq4s", "wifi7-current", "FPT SpeedX2 Eyes3 IQ4S", "1.049.000đ/tháng", "2 Gbps", "2 Gbps", "Wi‑Fi 7 + Mesh + 2–5 Camera IQ4S", "Nhà cần nhiều camera ngoài trời", ["2 Gbps đối xứng", "2–5 Camera IQ4S", "ZPlay"], FAMILY),
    offer("speedx2-eyes3-play4", "wifi7-current", "FPT SpeedX2 Eyes3 Play4", "1.049.000đ/tháng", "2 Gbps", "2 Gbps", "Wi‑Fi 7 + Mesh + 2–5 Camera Play4", "Nhà cần nhiều camera trong nhà", ["2 Gbps đối xứng", "2–5 Camera Play4", "ZPlay"], FAMILY),
    offer("speedx2-eyes3-play3", "wifi7-current", "FPT SpeedX2 Eyes3 Play3", "1.049.000đ/tháng", "2 Gbps", "2 Gbps", "Wi‑Fi 7 + Mesh + 2–5 Camera Play3", "Người dùng vẫn chọn hệ Camera Play3", ["2 Gbps đối xứng", "2–5 Camera Play3", "ZPlay"], FAMILY),
    offer("speedx2-pro-lite", "wifi7-current", "FPT SpeedX2 Pro Lite", "1.099.000đ/tháng", "2 Gbps", "2 Gbps", "Wi‑Fi 7 + Mesh", "Nhà lớn cần Wi‑Fi 7 Pro không gắn camera", ["2 Gbps đối xứng", "01 Mesh Wi‑Fi 7", "Cấu hình Pro Lite"], PLAY),
    offer("speedx10-play4", "wifi7-current", "FPT SpeedX10 - Play4", "1.639.000đ/tháng", "10 Gbps", "10 Gbps", "Wi‑Fi 7 + Mesh + Camera Play4", "Nhà/studio tải cực cao + camera", ["10 Gbps đối xứng", "Camera Play4", "ZPlay"], INTERNET),
    offer("speedx10-iq4s", "wifi7-current", "FPT SpeedX10 - IQ4S", "1.639.000đ/tháng", "10 Gbps", "10 Gbps", "Wi‑Fi 7 + Mesh + Camera IQ4S", "Nhà/studio tải cực cao + camera ngoài trời", ["10 Gbps đối xứng", "Camera IQ4S", "ZPlay"], INTERNET),
    offer("speedx10-pro-play4", "wifi7-current", "FPT SpeedX10 Pro - Play4", "1.699.000đ/tháng", "10 Gbps", "10 Gbps", "Wi‑Fi 7 + Mesh + Play4 + FPT Play", "Không gian lớn cần 10 Gbps, camera và FPT Play", ["10 Gbps đối xứng", "Camera Play4", "FPT Play VIP & Box650"], INTERNET),
    offer("speedx10-pro-iq4s", "wifi7-current", "FPT SpeedX10 Pro - IQ4S", "1.699.000đ/tháng", "10 Gbps", "10 Gbps", "Wi‑Fi 7 + Mesh + IQ4S + FPT Play", "Không gian lớn cần 10 Gbps và camera ngoài trời", ["10 Gbps đối xứng", "Camera IQ4S", "FPT Play VIP & Box650"], INTERNET),
    offer("speedx10-eyes3-iq4s", "wifi7-current", "FPT SpeedX10 Eyes3 IQ4S", "1.649.000đ/tháng", "10 Gbps", "10 Gbps", "Wi‑Fi 7 + Mesh + 2–5 Camera IQ4S", "Nhà/văn phòng tải cực cao + nhiều camera", ["10 Gbps đối xứng", "2–5 Camera IQ4S", "ZPlay"], FAMILY),
    offer("speedx10-eyes3-play4", "wifi7-current", "FPT SpeedX10 Eyes3 Play4", "1.649.000đ/tháng", "10 Gbps", "10 Gbps", "Wi‑Fi 7 + Mesh + 2–5 Camera Play4", "Nhà/văn phòng tải cực cao + nhiều camera trong nhà", ["10 Gbps đối xứng", "2–5 Camera Play4", "ZPlay"], FAMILY),
    offer("speedx10-pro-lite", "wifi7-current", "FPT SpeedX10 Pro Lite", "1.699.000đ/tháng", "10 Gbps", "10 Gbps", "Wi‑Fi 7 + Mesh", "Studio/văn phòng cần 10 Gbps Pro", ["10 Gbps đối xứng", "01 Mesh Wi‑Fi 7", "Cấu hình Pro Lite"], PLAY),
]

# Stale camera device/combo display prices from the previous snapshot.
PRICE_CORRECTIONS = {
    "camera-fpt": "Từ 500.000đ",
    "play4": "Từ 500.000đ",
    "iq4s": "Từ 500.000đ",
    "camera-2": "Từ 1.000.000đ",
    "camera-3": "Từ 1.500.000đ",
    "camera-5": "Từ 2.500.000đ",
    "camera-2-mix": "Từ 1.000.000đ",
    "camera-2-in": "Từ 1.000.000đ",
    "camera-2-out": "Từ 1.000.000đ",
    "camera-3-in": "Từ 1.500.000đ",
    "camera-3-out": "Từ 1.500.000đ",
    "camera-3-2in1out": "Từ 1.500.000đ",
    "camera-3-1in2out": "Từ 1.500.000đ",
}

GROUP_LABELS = {
    "official-play": ("FPT Play, V.VIP & combo thể thao", "Gói giải trí độc lập và combo Internet + FPT Play đang được niêm yết trên catalog FPT."),
    "business": ("Internet FPT cho doanh nghiệp", "Lux và Super Biz được tách riêng để người dùng cửa hàng, văn phòng và doanh nghiệp không phải chọn nhầm gói dân dụng."),
    "camera-current": ("Internet + Camera An Tâm 7", "Các cấu hình Camera Play4/IQ4S và Cloud An Tâm 7 không bị gộp vào một dòng chung."),
    "wifi7-current": ("Wi‑Fi 7 + Camera / giải trí", "Các biến thể SpeedX2/SpeedX10 với Camera, Mesh, ZPlay hoặc FPT Play được trình bày riêng."),
}


def location_name(html: str) -> str:
    match = re.search(r'<h1[^>]*>\s*Lắp mạng FPT tại\s+(.*?)</h1>', html, flags=re.I | re.S)
    if not match:
        return "khu vực của bạn"
    return re.sub(r'<[^>]+>', '', unescape(match.group(1))).strip()


def card(item: dict, location: str) -> str:
    benefits = ''.join(f'<li><span aria-hidden="true">✓</span><strong>{escape(x)}</strong></li>' for x in item['benefits'])
    return f'''<article class="local-plan-card-full official-extra-plan-card" data-official-extra-plan-card data-current-plan-id="{escape(item['id'])}" data-current-plan-group="{escape(item['group'])}">
<div class="local-plan-full-head"><div class="local-plan-full-title"><span class="local-plan-badge">Catalog FPT hiện hành</span><span class="local-plan-code">{escape(item['id'].upper())}</span><h3>{escape(item['name'])}</h3><p>Gói/dịch vụ được tách riêng để so sánh đầy đủ tại {escape(location)}.</p></div><div class="local-plan-full-price"><small>Giá niêm yết tham khảo</small><strong>{escape(item['price'])}</strong><span>FPT ghi giá có thể đổi theo khu vực và thời điểm</span></div></div>
<div class="local-plan-full-metrics"><div><span>DOWNLOAD / LOẠI</span><strong>{escape(item['down'])}</strong></div><div><span>UPLOAD</span><strong>{escape(item['up'])}</strong></div><div><span>THIẾT BỊ</span><strong>{escape(item['device'])}</strong></div><div><span>PHÙ HỢP</span><strong>{escape(item['fit'])}</strong></div></div>
<div class="local-plan-full-content"><div class="local-plan-panel"><h4>Quyền lợi & cấu hình</h4><ul class="local-plan-benefit-list">{benefits}</ul></div><div class="local-plan-panel"><h4>Điều kiện áp dụng</h4><p>Không suy diễn mức niêm yết thành báo giá cố định cho toàn {escape(location)}. Giá, thiết bị, chương trình tặng kèm và khả năng triển khai phải được xác nhận lại theo địa chỉ và thời điểm.</p></div></div>
<div class="local-plan-contract"><h4>Trước khi chốt gói</h4><div class="local-plan-contract-grid"><div><span>Giá cước</span><strong>Đối chiếu theo địa chỉ.</strong></div><div><span>Thiết bị</span><strong>Xác nhận model và số lượng.</strong></div><div><span>Ưu đãi</span><strong>Chỉ ghi nhận khi chương trình còn hiệu lực.</strong></div><div><span>Hạ tầng</span><strong>Kiểm tra đến địa chỉ cụ thể.</strong></div><div><span>Nhóm gói</span><strong>{escape(item['group'])}</strong></div><div><span>Ngày đối chiếu</span><strong>{OBSERVED_AT}</strong></div></div></div>
<div class="local-plan-register"><div><h4>Kiểm tra {escape(item['name'])} tại {escape(location)}</h4><ol><li>Chọn gói.</li><li>Gửi địa chỉ + số điện thoại.</li><li>Nhận xác nhận hạ tầng, giá, thiết bị và ưu đãi trước khi chốt.</li></ol></div><div class="local-plan-actions"><a class="btn btn-primary" href="#dang-ky" data-select-current-plan="{escape(item['name'])}">Chọn gói này</a><a class="btn btn-secondary" href="{escape(item['source'])}" rel="nofollow noopener" target="_blank">Nguồn FPT</a></div></div>
</article>'''


def correction_pattern(pid: str) -> re.Pattern[str]:
    return re.compile(
        rf'(<article\b(?=[^>]*(?:data-plan-id|data-current-plan-id)=["\']{re.escape(pid)}["\'])[^>]*>.*?<div class="local-plan-full-price">.*?<strong>)(.*?)(</strong>)',
        flags=re.I | re.S,
    )


def correct_prices(html: str) -> str:
    for pid, price in PRICE_CORRECTIONS.items():
        pattern = correction_pattern(pid)
        html, changed = pattern.subn(lambda m: m.group(1) + escape(price) + m.group(3), html, count=1)
        if changed != 1:
            raise SystemExit(f"OFFICIAL CATALOG BUILD FAIL: cannot correct price for {pid}")
    return html


def build_block(location: str) -> str:
    groups = []
    for key in ("official-play", "business", "camera-current", "wifi7-current"):
        title, intro = GROUP_LABELS[key]
        items = [x for x in OFFERS if x['group'] == key]
        groups.append(f'''<div class="local-plan-group official-extra-group" data-official-extra-group="{key}"><div class="local-plan-group-head"><h3>{escape(title)}</h3><p>{escape(intro)}</p></div><div class="local-plan-grid">{''.join(card(x, location) for x in items)}</div></div>''')
    return f'''<div class="official-extra-catalog" data-official-extra-catalog="{len(OFFERS)}" data-official-extra-observed="{OBSERVED_AT}"><div class="local-current-offerings-head"><span class="eyebrow">Catalog đối chiếu 18/08/2026</span><h3>Bổ sung {len(OFFERS)} lựa chọn FPT còn thiếu</h3><p>Gồm FPT Play/V.VIP, doanh nghiệp, Camera An Tâm 7 và Wi‑Fi 7. Các biến thể được FPT ghi rõ chỉ áp dụng Tây Nam Bộ không được áp dụng đại trà cho 34 tỉnh/thành.</p></div>{''.join(groups)}</div>'''


def inject(path: Path) -> None:
    html = path.read_text(encoding='utf-8')
    if 'data-official-extra-catalog=' in html:
        raise SystemExit(f"OFFICIAL CATALOG BUILD FAIL: duplicate official catalog in {path}")
    if html.count('local-plan-card-full') < EXPECTED_BASE:
        raise SystemExit(f"OFFICIAL CATALOG BUILD FAIL: base rich cards missing in {path}")
    html = correct_prices(html)
    marker = '<div class="local-catalog-source">'
    if marker not in html:
        raise SystemExit(f"OFFICIAL CATALOG BUILD FAIL: source marker missing in {path}")
    html = html.replace(marker, build_block(location_name(html)) + marker, 1)
    path.write_text(html, encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    pages = sorted((Path(args.site) / 'khu-vuc').glob('*/index.html'))
    if len(pages) != 34:
        raise SystemExit(f"OFFICIAL CATALOG BUILD FAIL: expected 34 province pages, got {len(pages)}")
    for page in pages:
        inject(page)
    total = EXPECTED_BASE + len(OFFERS)
    print(f"OFFICIAL CATALOG BUILT: 34/34 provinces × {total} rich offers = {34 * total}; added={len(OFFERS)} current official offers/province; stale camera prices corrected; Tây Nam Bộ-only variants excluded")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
