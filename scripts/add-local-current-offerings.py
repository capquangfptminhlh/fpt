from __future__ import annotations

import argparse
import re
from html import escape, unescape
from pathlib import Path

OBSERVED_AT = "2026-08-18"

INTERNET_SOURCE = "https://fpt.vn/internet/ca-nhan"
FAMILY_SOURCE = "https://fpt.vn/internet/gia-dinh"
FGAME_F1_SOURCE = "https://fpt.vn/internet/goi-combo-f-game-f1"
CAMERA_SOURCE = "https://fpt.vn/camera"


def plan(pid, group, name, price, down, up, device, fit, benefits, source):
    return {
        "id": pid, "group": group, "name": name, "price": price, "down": down, "up": up,
        "device": device, "fit": fit, "benefits": benefits, "source": source,
    }


PLANS = [
    plan("giga-f1", "internet", "Internet GIGA F1", "205.000đ/tháng", "300 Mbps; X3 có thể 1 Gbps", "300 Mbps", "Modem Wi‑Fi 6 + 1 Access Point", "Nhà ít tầng cần thêm vùng phủ", ["1 Access Point mở rộng vùng phủ", "Kết nối đến 15 thiết bị theo nguồn FPT", "Có chương trình Camera + Cloud tùy thời điểm"], INTERNET_SOURCE),
    plan("giga-f2", "internet", "Internet GIGA F2", "225.000đ/tháng", "300 Mbps", "300 Mbps", "Modem Wi‑Fi 6 + 2 Access Point", "Nhà nhiều phòng/tầng", ["2 Access Point", "Băng thông đối xứng nền 300 Mbps", "Giá/ưu đãi xác nhận theo địa chỉ"], INTERNET_SOURCE),
    plan("giga-f3", "internet", "Internet GIGA F3", "245.000đ/tháng", "300 Mbps", "300 Mbps", "Modem Wi‑Fi 6 + 3 Access Point", "Nhà nhiều tầng, diện tích rộng", ["3 Access Point", "Phủ Wi‑Fi nhiều khu vực", "Phù hợp nhà cần nhiều điểm phát"], FAMILY_SOURCE),
    plan("sky-f1", "internet", "Internet SKY F1", "210.000đ/tháng", "1 Gbps", "300 Mbps; X3 có thể 1 Gbps", "Modem Wi‑Fi 6 + 1 Access Point", "Nhà ít tầng, nhiều thiết bị", ["1 Access Point", "Download đến 1 Gbps", "Kết nối lên đến 25 thiết bị theo nguồn FPT"], INTERNET_SOURCE),
    plan("sky-f2", "internet", "Internet SKY F2", "230.000đ/tháng", "1 Gbps", "300 Mbps; X3 có thể 1 Gbps", "Modem Wi‑Fi 6 + 2 Access Point", "Nhà nhiều tầng, không gian rộng", ["2 Access Point", "Download đến 1 Gbps", "Phủ sóng mạnh cho nhà nhiều tầng"], INTERNET_SOURCE),
    plan("sky-f3", "internet", "Internet SKY F3", "255.000đ/tháng", "1 Gbps", "300 Mbps; X3 có thể 1 Gbps", "Modem Wi‑Fi 6 + 3 Access Point", "Nhà lớn cần phủ Wi‑Fi tối đa", ["3 Access Point", "Kết nối nhiều thiết bị", "Phủ sóng nhiều tầng"], INTERNET_SOURCE),
    plan("meta-f1", "internet", "Internet META F1", "315.000đ/tháng", "1 Gbps", "1 Gbps", "Modem Wi‑Fi 6 + 1 Access Point", "Upload cao + nhà ít tầng", ["Băng thông 1 Gbps đối xứng", "1 Access Point", "Kết nối đến 25 thiết bị"], INTERNET_SOURCE),
    plan("meta-f2", "internet", "Internet META F2", "335.000đ/tháng", "1 Gbps", "1 Gbps", "Modem Wi‑Fi 6 + 2 Access Point", "Upload cao + nhà nhiều tầng", ["Băng thông 1 Gbps đối xứng", "2 Access Point", "Phủ sóng mạnh cho không gian rộng"], INTERNET_SOURCE),
    plan("meta-f3", "internet", "Internet META F3", "355.000đ/tháng", "1 Gbps", "1 Gbps", "Modem Wi‑Fi 6 + 3 Access Point", "Nhà lớn, creator, cloud", ["Băng thông 1 Gbps đối xứng", "3 Access Point", "Phủ sóng tối đa cho nhà nhiều tầng"], INTERNET_SOURCE),
    plan("fpt-an-tam", "internet", "FPT An Tâm", "195.000đ/tháng", "300 Mbps", "300 Mbps", "Modem Wi‑Fi 6 + F‑Safe", "Gia đình có trẻ em, ưu tiên an toàn số", ["F‑Safe chặn website độc hại/lừa đảo", "Quản lý thời gian truy cập", "Quản lý nội dung truy cập của trẻ em"], INTERNET_SOURCE),
    plan("f-game-f1", "internet", "Internet F‑Game F1", "245.000đ/tháng", "1 Gbps", "300 Mbps", "Wi‑Fi 6 + 1 Access Point + Ultra Fast", "Game thủ cần thêm vùng phủ", ["Ultra Fast hỗ trợ 50+ game", "1 Access Point", "Giảm độ trễ theo điều kiện mạng thực tế"], INTERNET_SOURCE),

    plan("combo-giga-f1", "combo", "Combo GIGA F1 + FPT Play", "220.000đ/tháng", "300 Mbps; X3 có thể 1 Gbps", "300 Mbps", "Wi‑Fi 6 + FPT Play Box + 1 Access Point", "Internet + TV + nhà ít tầng", ["FPT Play Box", "1 Access Point", "Gần 120 kênh theo nguồn FPT hiện hành"], INTERNET_SOURCE),
    plan("combo-sky-f1", "combo", "Combo SKY F1 + FPT Play", "239.000đ/tháng", "1 Gbps", "300 Mbps; X3 có thể 1 Gbps", "Wi‑Fi 6 + FPT Play Box + 1 Access Point", "Nhiều thiết bị + TV", ["FPT Play Box", "1 Access Point", "Gần 120 kênh truyền hình"], INTERNET_SOURCE),
    plan("combo-sky-f2", "combo", "Combo SKY F2 + FPT Play", "259.000đ/tháng", "1 Gbps", "300 Mbps; X3 có thể 1 Gbps", "Wi‑Fi 6 + FPT Play Box + 2 Access Point", "Nhà nhiều tầng + giải trí", ["FPT Play Box", "2 Access Point", "Gần 120 kênh truyền hình"], INTERNET_SOURCE),
    plan("combo-sky-f3", "combo", "Combo SKY F3 + FPT Play", "280.000đ/tháng", "1 Gbps", "300 Mbps; X3 có thể 1 Gbps", "Wi‑Fi 6 + FPT Play Box + 3 Access Point", "Nhà lớn + giải trí", ["FPT Play Box", "3 Access Point", "Phủ Wi‑Fi nhiều tầng"], INTERNET_SOURCE),
    plan("combo-meta-f1", "combo", "Combo META F1 + FPT Play", "340.000đ/tháng", "1 Gbps", "1 Gbps", "Wi‑Fi 6 + FPT Play Box + 1 Access Point", "Upload cao + TV + nhà ít tầng", ["Băng thông đối xứng", "FPT Play Box", "Tặng/đi kèm 1 Access Point theo cấu hình nguồn"], INTERNET_SOURCE),
    plan("combo-meta-f2", "combo", "Combo META F2 + FPT Play", "360.000đ/tháng", "1 Gbps", "1 Gbps", "Wi‑Fi 6 + FPT Play Box + 2 Access Point", "Upload cao + TV + nhà nhiều tầng", ["Băng thông đối xứng", "FPT Play Box", "2 Access Point"], INTERNET_SOURCE),
    plan("combo-meta-f3", "combo", "Combo META F3 + FPT Play", "380.000đ/tháng", "1 Gbps", "1 Gbps", "Wi‑Fi 6 + FPT Play Box + 3 Access Point", "Nhà lớn, upload cao + TV", ["Băng thông đối xứng", "FPT Play Box", "3 Access Point"], INTERNET_SOURCE),
    plan("combo-giga-f2-lite", "combo", "Combo GIGA F2 Lite", "249.000đ/tháng", "300 Mbps; X3 có thể 1 Gbps", "300 Mbps", "Wi‑Fi 6 + FPT Play + 2 Access Point", "Nhà nhiều phòng cần combo tiết kiệm", ["2 Access Point", "Gần 120 kênh truyền hình", "Camera + Cloud có thể thuộc chương trình hiện hành"], INTERNET_SOURCE),
    plan("combo-giga-f3-lite", "combo", "Combo GIGA F3 Lite", "269.000đ/tháng", "1 Gbps theo X3 hiện hành", "300 Mbps", "Wi‑Fi 6 + FPT Play + 3 Access Point", "Nhà nhiều tầng cần nhiều điểm phát", ["3 Access Point", "Gần 120 kênh truyền hình", "Giá/ưu đãi xác nhận theo địa chỉ"], INTERNET_SOURCE),
    plan("combo-meta-f1-lite", "combo", "Combo META F1 Lite", "325.000đ/tháng", "1 Gbps", "1 Gbps", "Wi‑Fi 6 + FPT Play + Access Point/Mesh", "Upload cao + giải trí", ["1 Access Point theo nguồn FPT", "1 Wi‑Fi Mesh theo cấu hình nguồn", "Gần 120 kênh truyền hình"], INTERNET_SOURCE),
    plan("combo-meta-f2-lite", "combo", "Combo META F2 Lite", "355.000đ/tháng", "1 Gbps", "1 Gbps", "Wi‑Fi 6 + FPT Play + 2 Access Point", "Nhà nhiều tầng + upload cao", ["2 Access Point", "Gần 120 kênh truyền hình", "Thiết bị cuối cùng xác nhận theo địa chỉ"], INTERNET_SOURCE),
    plan("combo-f-game-f1", "combo", "Combo F‑Game F1 + FPT Play", "290.000đ/tháng", "1 Gbps", "300 Mbps", "Wi‑Fi 6 + Access Point + FPT Play Box + Ultra Fast", "Game thủ + TV + thêm vùng phủ", ["Ultra Fast hỗ trợ 50+ game", "FPT Play Box", "1 Access Point"], FGAME_F1_SOURCE),

    plan("camera-2-mix", "camera", "Combo 2 Camera Trong + Ngoài", "Từ 950.000đ", "2 Camera", "—", "01 Camera trong + 01 Camera ngoài", "Nhà/cửa hàng cần quan sát hai vùng", ["Cấu hình trong + ngoài", "Quản lý tập trung", "Cloud tùy gói"], CAMERA_SOURCE),
    plan("camera-2-in", "camera", "Combo 2 Camera Trong Nhà", "Từ 950.000đ", "2 Camera", "—", "02 Camera trong nhà", "Căn hộ, nhà nhỏ, cửa hàng", ["2 vị trí trong nhà", "Quản lý tập trung", "Cloud tùy gói"], CAMERA_SOURCE),
    plan("camera-2-out", "camera", "Combo 2 Camera Ngoài Trời", "Từ 950.000đ", "2 Camera", "—", "02 Camera ngoài trời", "Cổng, sân, mặt tiền", ["2 vị trí ngoài trời", "Quản lý tập trung", "Cloud tùy gói"], CAMERA_SOURCE),
    plan("camera-3-in", "camera", "Combo 3 Camera Trong Nhà", "Từ 1.150.000đ", "3 Camera", "—", "03 Camera trong nhà", "Nhà nhiều phòng/cửa hàng", ["3 vị trí trong nhà", "Quản lý tập trung", "Cloud tùy gói"], CAMERA_SOURCE),
    plan("camera-3-out", "camera", "Combo 3 Camera Ngoài Trời", "Từ 1.150.000đ", "3 Camera", "—", "03 Camera ngoài trời", "Nhà/cơ sở cần nhiều góc ngoài trời", ["3 vị trí ngoài trời", "Quản lý tập trung", "Cloud tùy gói"], CAMERA_SOURCE),
    plan("camera-3-2in1out", "camera", "Combo 3 Camera – 2 Trong + 1 Ngoài", "Từ 1.150.000đ", "3 Camera", "—", "02 trong nhà + 01 ngoài trời", "Nhà/cửa hàng cần giám sát hỗn hợp", ["2 camera trong", "1 camera ngoài", "Cloud tùy gói"], CAMERA_SOURCE),
    plan("camera-3-1in2out", "camera", "Combo 3 Camera – 1 Trong + 2 Ngoài", "Từ 1.150.000đ", "3 Camera", "—", "01 trong nhà + 02 ngoài trời", "Cơ sở có nhiều điểm ngoài trời", ["1 camera trong", "2 camera ngoài", "Cloud tùy gói"], CAMERA_SOURCE),
]

GROUP_LABELS = {
    "internet": ("Internet mở rộng F1–F3 & An Tâm", "Các biến thể vùng phủ, an toàn số và gaming còn thiếu trong catalog lõi."),
    "combo": ("Combo FPT Play F1–F3 & Lite", "Các biến thể Internet + FPT Play với Access Point/Mesh và F‑Game F1."),
    "camera": ("Đủ cấu hình combo Camera", "Tách riêng từng tổ hợp 2–3 Camera thay vì gom thành một dòng chung."),
}


def location_name(html: str) -> str:
    match = re.search(r'<h1[^>]*>\s*Lắp mạng FPT tại\s+(.*?)</h1>', html, flags=re.I | re.S)
    if not match:
        return "khu vực của bạn"
    return re.sub(r'<[^>]+>', '', unescape(match.group(1))).strip()


def card(item: dict, location: str) -> str:
    benefits = ''.join(f'<li><span aria-hidden="true">✓</span><strong>{escape(x)}</strong></li>' for x in item['benefits'])
    return f'''<article class="local-plan-card-full local-current-plan-card" data-local-current-plan-card data-current-plan-id="{escape(item['id'])}" data-current-plan-group="{escape(item['group'])}">
<div class="local-plan-full-head"><div class="local-plan-full-title"><span class="local-plan-badge">Bổ sung hiện hành</span><span class="local-plan-code">{escape(item['id'].upper())}</span><h3>{escape(item['name'])}</h3><p>Biến thể gói FPT được bổ sung từ catalog chính thức, trình bày đầy đủ ngay trên trang {escape(location)}.</p></div><div class="local-plan-full-price"><small>Giá tham khảo / chỉ từ</small><strong>{escape(item['price'])}</strong><span>Kiểm tra lại theo địa chỉ</span></div></div>
<div class="local-plan-full-metrics"><div><span>DOWNLOAD / CẤU HÌNH</span><strong>{escape(item['down'])}</strong></div><div><span>UPLOAD</span><strong>{escape(item['up'])}</strong></div><div><span>THIẾT BỊ</span><strong>{escape(item['device'])}</strong></div><div><span>PHÙ HỢP</span><strong>{escape(item['fit'])}</strong></div></div>
<div class="local-plan-full-content"><div class="local-plan-panel"><h4>Quyền lợi & cấu hình</h4><ul class="local-plan-benefit-list">{benefits}</ul></div><div class="local-plan-panel"><h4>Điều kiện áp dụng</h4><p>Giá, băng thông X3, thiết bị, khuyến mãi và khả năng triển khai có thể thay đổi theo khu vực/thời điểm. Không coi mức tham khảo này là báo giá cố định cho toàn {escape(location)}.</p></div></div>
<div class="local-plan-contract"><h4>Trước khi chốt gói</h4><div class="local-plan-contract-grid"><div><span>Giá cước</span><strong>Đối chiếu theo địa chỉ.</strong></div><div><span>VAT</span><strong>Nguồn FPT hiện hành ghi mức hiển thị đã bao gồm VAT ở các bảng giá tương ứng; kiểm tra lại báo giá cuối.</strong></div><div><span>Thiết bị</span><strong>Xác nhận model/số lượng thực tế.</strong></div><div><span>Khuyến mãi</span><strong>Chỉ áp dụng khi chương trình còn hiệu lực.</strong></div><div><span>Hạ tầng</span><strong>Kiểm tra đến số nhà cụ thể.</strong></div><div><span>Ngày đối chiếu</span><strong>{OBSERVED_AT}</strong></div></div></div>
<div class="local-plan-register"><div><h4>Đăng ký {escape(item['name'])} tại {escape(location)}</h4><ol><li>Chọn gói.</li><li>Gửi địa chỉ + số điện thoại.</li><li>Nhận xác nhận hạ tầng, giá, thiết bị và ưu đãi trước khi chốt.</li></ol></div><div class="local-plan-actions"><a class="btn btn-primary" href="#dang-ky" data-select-current-plan="{escape(item['name'])}">Chọn gói này</a><a class="btn btn-secondary" href="{escape(item['source'])}" rel="nofollow noopener" target="_blank">Nguồn FPT</a></div></div>
</article>'''


def block(location: str) -> str:
    groups = []
    for key in ("internet", "combo", "camera"):
        title, intro = GROUP_LABELS[key]
        items = [x for x in PLANS if x['group'] == key]
        groups.append(f'''<div class="local-plan-group local-current-group" data-current-group="{key}"><div class="local-plan-group-head"><h3>{escape(title)}</h3><p>{escape(intro)}</p></div><div class="local-plan-grid">{''.join(card(x, location) for x in items)}</div></div>''')
    return f'''<div class="local-current-offerings" data-current-offerings="{len(PLANS)}" data-current-offerings-observed="{OBSERVED_AT}"><div class="local-current-offerings-head"><span class="eyebrow">Bổ sung từ catalog FPT hiện hành</span><h3>Thêm {len(PLANS)} biến thể gói còn thiếu</h3><p>Không đưa các cấu hình được FPT ghi rõ chỉ áp dụng Tây Nam Bộ vào catalog chung của 34 tỉnh/thành.</p></div>{''.join(groups)}</div>'''


def inject(path: Path) -> None:
    html = path.read_text(encoding='utf-8')
    if 'data-current-offerings=' in html:
        return
    marker = '<div class="local-catalog-source">'
    if marker not in html:
        raise SystemExit(f'CURRENT OFFERINGS BUILD FAIL: source marker missing in {path}')
    location = location_name(html)
    html = html.replace(marker, block(location) + marker, 1)
    path.write_text(html, encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    pages = sorted((Path(args.site) / 'khu-vuc').glob('*/index.html'))
    if len(pages) != 34:
        raise SystemExit(f'CURRENT OFFERINGS BUILD FAIL: expected 34 province pages, got {len(pages)}')
    for page in pages:
        inject(page)
    print(f'Current offerings added: 34 provinces × {len(PLANS)} missing variants = {34 * len(PLANS)} extra full blocks; total visible full package blocks/province = {26 + len(PLANS)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
