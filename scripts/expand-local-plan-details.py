from __future__ import annotations

import argparse
import re
from html import escape, unescape
from pathlib import Path

OBSERVED_AT = "2026-08-18"


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", unescape(value))).strip()


def capture(pattern: str, text: str, default: str = "") -> str:
    m = re.search(pattern, text, flags=re.I | re.S)
    return clean(m.group(1)) if m else default


def speed_parts(speed: str) -> tuple[str, str]:
    if "/" in speed:
        a, b = [x.strip() for x in speed.split("/", 1)]
        return a, b
    if "camera" in speed.lower() or "dịch vụ" in speed.lower() or "thiết bị" in speed.lower():
        return speed, "—"
    return speed, "Theo gói"


def parse_features(card: str) -> list[str]:
    block = re.search(r'<ul class="local-plan-features">(.*?)</ul>', card, flags=re.I | re.S)
    if not block:
        return []
    return [clean(x) for x in re.findall(r'<li[^>]*>(.*?)</li>', block.group(1), flags=re.I | re.S) if clean(x)]


def full_card(card: str, location: str) -> str:
    attrs = capture(r'<article\b([^>]*)>', card)
    plan_id = capture(r'data-plan-id=["\']([^"\']+)', attrs, "plan")
    kind = capture(r'data-local-product=["\']([^"\']+)', attrs, "internet")
    badge = capture(r'<span class="local-plan-badge">(.*?)</span>', card, kind)
    name = capture(r'<h3>(.*?)</h3>', card, "Gói FPT")
    price = capture(r'<p class="local-plan-price">.*?<strong>(.*?)</strong>', card, "Kiểm tra theo địa chỉ")
    speed = capture(r'<div class="local-plan-specs">.*?<span>Tốc độ / loại</span><strong>(.*?)</strong>', card, "Theo gói")
    device = capture(r'<span>Thiết bị</span><strong>(.*?)</strong>', card, "Theo cấu hình gói")
    fit = capture(r'<p class="local-plan-fit">.*?</strong>(.*?)</p>', card, "Tùy nhu cầu sử dụng")
    detail_href = capture(r'<a class="btn btn-secondary" href="([^"]+)">', card, "#dang-ky")
    features = parse_features(card)
    down, up = speed_parts(speed)
    feature_html = "".join(f'<li><span aria-hidden="true">✓</span><strong>{escape(x)}</strong></li>' for x in features)
    if not feature_html:
        feature_html = '<li><span aria-hidden="true">✓</span><strong>Thông tin thiết bị và quyền lợi cần xác nhận theo địa chỉ.</strong></li>'

    if kind.startswith("camera"):
        use_label = "Cấu hình camera"
        use_value = speed
    elif kind.startswith("play"):
        use_label = "Dịch vụ chính"
        use_value = "Internet + FPT Play"
    else:
        use_label = "Loại gói"
        use_value = "Internet FPT"

    return f'''<article class="local-plan-card local-plan-card-full" data-local-plan-card data-local-product="{escape(kind)}" data-plan-id="{escape(plan_id)}">
<div class="local-plan-full-head"><div class="local-plan-full-title"><span class="local-plan-badge">{escape(badge)}</span><span class="local-plan-code">{escape(plan_id.upper())}</span><h3>{escape(name)}</h3><p>Gói được trình bày đầy đủ ngay tại trang {escape(location)} — không cần mở trang khác mới biết cấu hình chính.</p></div><div class="local-plan-full-price"><small>Giá tham khảo / chỉ từ</small><strong>{escape(price)}</strong><span>Giá cuối cùng xác nhận theo địa chỉ</span></div></div>
<div class="local-plan-full-metrics"><div><span>DOWNLOAD / TỐC ĐỘ</span><strong>{escape(down)}</strong></div><div><span>UPLOAD</span><strong>{escape(up)}</strong></div><div><span>{escape(use_label)}</span><strong>{escape(use_value)}</strong></div><div><span>THIẾT BỊ</span><strong>{escape(device)}</strong></div></div>
<div class="local-plan-full-content"><section class="local-plan-panel"><h4>Quyền lợi & cấu hình đi kèm</h4><ul class="local-plan-benefit-list">{feature_html}</ul></section><section class="local-plan-panel"><h4>Gói này phù hợp với ai?</h4><p>{escape(fit)}</p><div class="local-plan-use-cases"><span>Gia đình</span><span>Nhà phố / căn hộ</span><span>Nhiều thiết bị</span><span>Kiểm tra hạ tầng trước</span></div></section></div>
<div class="local-plan-contract"><h4>Thông tin cần biết trước khi đăng ký</h4><div class="local-plan-contract-grid"><div><span>Giá cước</span><strong>Mức tham khảo từ nguồn FPT, có thể đổi theo khu vực/thời điểm.</strong></div><div><span>VAT & chi phí khác</span><strong>Đối chiếu lại báo giá cuối cùng; một số dịch vụ có thể có phí thiết bị/dịch vụ gia tăng.</strong></div><div><span>Thiết bị thực tế</span><strong>Modem, Box, Access Point, Mesh hoặc Camera có thể khác theo khu vực và tồn kho.</strong></div><div><span>Khuyến mãi</span><strong>Chỉ áp dụng khi chương trình còn hiệu lực và địa chỉ đáp ứng điều kiện.</strong></div><div><span>Hạ tầng</span><strong>Phải kiểm tra đến số nhà/địa chỉ cụ thể tại {escape(location)}.</strong></div><div><span>Ngày đối chiếu</span><strong>{OBSERVED_AT}</strong></div></div></div>
<div class="local-plan-register"><div><h4>Đăng ký {escape(name)} tại {escape(location)}</h4><ol><li>Chọn gói này.</li><li>Gửi số điện thoại + địa chỉ lắp đặt.</li><li>Kiểm tra hạ tầng, thiết bị, giá và ưu đãi thực tế trước khi chốt.</li></ol></div><div class="local-plan-actions"><a class="btn btn-primary" href="#dang-ky" data-select-local-plan="{escape(name)}">Chọn {escape(name)}</a><a class="btn btn-secondary" href="{escape(detail_href)}">Xem trang gói gốc</a></div></div>
</article>'''


def expand(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    location = capture(r'<h1[^>]*>\s*Lắp mạng FPT tại\s+(.*?)</h1>', html, path.parent.name)
    section = re.search(r'<section\b(?=[^>]*\blocal-commerce\b)[^>]*>.*?</section>', html, flags=re.I | re.S)
    if not section:
        raise SystemExit(f"LOCAL FULL PLAN BUILD FAIL: commerce section missing in {path}")
    block = section.group(0)
    cards = list(re.finditer(r'<article class="local-plan-card"[^>]*>.*?</article>', block, flags=re.I | re.S))
    if len(cards) != 26:
        raise SystemExit(f"LOCAL FULL PLAN BUILD FAIL: expected 26 base cards in {path}, got {len(cards)}")
    out, pos = [], 0
    for m in cards:
        out.append(block[pos:m.start()])
        out.append(full_card(m.group(0), location))
        pos = m.end()
    out.append(block[pos:])
    rich = ''.join(out).replace('data-catalog-observed="2026-08-18"', 'data-catalog-observed="2026-08-18" data-full-plan-details="true"', 1)
    html = html[:section.start()] + rich + html[section.end():]
    css = '<link rel="stylesheet" href="../../assets/css/local-catalog-full.css" data-local-catalog-full-style="v2"/>'
    if 'data-local-catalog-full-style=' not in html:
        html = html.replace('</head>', css + '</head>', 1)
    path.write_text(html, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    root = Path(args.site) / 'khu-vuc'
    pages = sorted(root.glob('*/index.html'))
    if len(pages) != 34:
        raise SystemExit(f"LOCAL FULL PLAN BUILD FAIL: expected 34 province pages, got {len(pages)}")
    for page in pages:
        expand(page)
    print('Local full plan details rendered: 34 provinces × 26 complete package blocks = 884 full package presentations')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
