from __future__ import annotations

import argparse
import re
from html import escape, unescape
from pathlib import Path


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", unescape(value))).strip()


def capture(pattern: str, text: str, default: str = "") -> str:
    match = re.search(pattern, text, flags=re.I | re.S)
    return clean(match.group(1)) if match else default


def attr(card: str, name: str, default: str = "") -> str:
    return capture(rf'{re.escape(name)}=["\']([^"\']+)', card, default)


def metric_pairs(card: str) -> list[tuple[str, str]]:
    block = re.search(r'<div class="local-plan-full-metrics">(.*?)</div>\s*<div class="local-plan-full-content">', card, flags=re.I | re.S)
    if not block:
        return []
    return [
        (clean(label), clean(value))
        for label, value in re.findall(r'<div><span>(.*?)</span><strong>(.*?)</strong></div>', block.group(1), flags=re.I | re.S)
    ]


def benefits(card: str) -> list[str]:
    block = re.search(r'<ul class="local-plan-benefit-list">(.*?)</ul>', card, flags=re.I | re.S)
    if not block:
        return []
    rows = re.findall(r'<li[^>]*>(.*?)</li>', block.group(1), flags=re.I | re.S)
    return [clean(row) for row in rows if clean(row)]


def tone(name: str, kind: str, plan_id: str) -> tuple[str, str, str]:
    key = f"{name} {kind} {plan_id}".lower()
    if "speedx" in key or "wifi 7" in key:
        return "premium-tone-electric", "Wi‑Fi 7", "✦"
    if "f-game" in key or "f‑game" in key or "game" in key:
        return "premium-tone-gaming", "Gaming", "⚡"
    if "camera" in key:
        return "premium-tone-camera", "Camera AI", "◉"
    if "meta" in key:
        return "premium-tone-violet", "Đề xuất", "♛"
    if "sky" in key:
        return "premium-tone-blue", "Phổ biến", "★"
    if "combo" in key or kind in {"combo", "play", "play-extra"}:
        return "premium-tone-blue", "Combo", "✦"
    return "premium-tone-orange", "Giá tốt", "⚡"


def pick_metric(pairs: list[tuple[str, str]], keys: tuple[str, ...], fallback: str) -> str:
    for label, value in pairs:
        normalized = label.lower()
        if any(key in normalized for key in keys):
            return value
    return fallback


def render_card(card: str, location: str, index: int) -> str:
    plan_id = attr(card, "data-plan-id") or attr(card, "data-current-plan-id") or f"plan-{index}"
    kind = attr(card, "data-local-product") or attr(card, "data-current-plan-group") or "internet"
    name = capture(r'<h3>(.*?)</h3>', card, "Gói Internet FPT")
    price = capture(r'<div class="local-plan-full-price">.*?<strong>(.*?)</strong>', card, "Kiểm tra theo địa chỉ")
    pairs = metric_pairs(card)
    download = pairs[0][1] if pairs else "Theo gói"
    upload = pairs[1][1] if len(pairs) > 1 else "Theo gói"
    device = pick_metric(pairs, ("thiết bị",), "Thiết bị theo gói")
    fit = pick_metric(pairs, ("phù hợp",), "Gia đình và nhu cầu thực tế")
    if fit == "Gia đình và nhu cầu thực tế":
        fit = capture(r'<div class="local-plan-panel"><h4>Gói này phù hợp với ai\?</h4><p>(.*?)</p>', card, fit)
    items = benefits(card)
    if not items:
        items = ["Cấu hình linh hoạt theo nhu cầu", "Hỗ trợ kỹ thuật 24/7", "Kiểm tra khả dụng tại địa chỉ lắp đặt"]
    front_items = items[:3]
    all_items = items[:6]
    style, badge, icon = tone(name, kind, plan_id)
    featured = " is-featured" if badge in {"Phổ biến", "Đề xuất", "Wi‑Fi 7"} else ""
    detail_id = f"premium-detail-{re.sub(r'[^a-z0-9-]+', '-', plan_id.lower()).strip('-')}-{index}"
    front_html = "".join(f'<li><span aria-hidden="true">✓</span>{escape(item)}</li>' for item in front_items)
    all_html = "".join(f'<li><span aria-hidden="true">✓</span>{escape(item)}</li>' for item in all_items)
    select_attr = "data-select-current-plan" if "data-current-plan-id=" in card else "data-select-local-plan"

    return f'''<article class="premium-plan-card {style}{featured}" data-premium-plan-card data-premium-plan-id="{escape(plan_id)}" data-premium-plan-name="{escape(name)}">
<div class="premium-plan-orb" aria-hidden="true">{escape(icon)}</div>
<div class="premium-plan-head"><span class="premium-plan-badge"><span aria-hidden="true">{escape(icon)}</span>{escape(badge)}</span><h3>{escape(name)}</h3><p class="premium-plan-kicker">Chỉ từ</p><p class="premium-plan-price"><strong>{escape(price)}</strong></p></div>
<div class="premium-plan-speed"><div><span class="premium-metric-label">Download</span><strong><i aria-hidden="true">↓</i>{escape(download)}</strong></div><span class="premium-speed-divider" aria-hidden="true"></span><div><span class="premium-metric-label">Upload</span><strong><i aria-hidden="true">↑</i>{escape(upload)}</strong></div></div>
<ul class="premium-plan-benefits">{front_html}</ul>
<div class="premium-plan-actions"><button type="button" class="premium-btn premium-btn-secondary" data-premium-plan-toggle aria-expanded="false" aria-controls="{escape(detail_id)}">Xem chi tiết</button><a class="premium-btn premium-btn-primary" href="#dang-ky" {select_attr}="{escape(name)}" data-premium-select-plan="{escape(name)}">Đăng ký ngay <span aria-hidden="true">→</span></a></div>
<div class="premium-plan-drawer" id="{escape(detail_id)}" hidden><div class="premium-plan-drawer-grid"><div><span class="premium-drawer-label">Thiết bị</span><strong>{escape(device)}</strong></div><div><span class="premium-drawer-label">Phù hợp</span><strong>{escape(fit)}</strong></div></div><h4>Quyền lợi nổi bật</h4><ul>{all_html}</ul><div class="premium-plan-notice"><strong>Kiểm tra theo địa chỉ</strong><span>Giá, thiết bị, hạ tầng và ưu đãi thực tế được xác nhận trước khi đăng ký.</span></div></div>
</article>'''


def premiumize(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    location = capture(r'<h1[^>]*>\s*Lắp mạng FPT tại\s+(.*?)</h1>', html, path.parent.name)
    section = re.search(r'<section\b(?=[^>]*\blocal-commerce\b)[^>]*>.*?</section>', html, flags=re.I | re.S)
    if not section:
        raise SystemExit(f"PREMIUM CATALOG BUILD FAIL: local commerce missing in {path}")
    block = section.group(0)
    article_re = re.compile(r'<article\b(?=[^>]*(?:local-plan-card-full|local-plan-card local-plan-card-full))[^>]*>.*?</article>', flags=re.I | re.S)
    cards = list(article_re.finditer(block))
    if len(cards) != 56:
        raise SystemExit(f"PREMIUM CATALOG BUILD FAIL: expected 56 rich cards in {path}, got {len(cards)}")

    parts: list[str] = []
    cursor = 0
    for index, match in enumerate(cards, start=1):
        parts.append(block[cursor:match.start()])
        parts.append(render_card(match.group(0), location, index))
        cursor = match.end()
    parts.append(block[cursor:])
    block = "".join(parts)

    block = re.sub(
        r'<div class="local-current-offerings-head">.*?</div>',
        '<div class="local-current-offerings-head premium-offerings-head"><span class="eyebrow">Thêm lựa chọn theo nhu cầu</span><h3>Gói mở rộng cho nhà nhiều tầng, giải trí, gaming & camera</h3><p>Chọn cấu hình phù hợp, sau đó kiểm tra khả dụng thực tế tại địa chỉ lắp đặt.</p></div>',
        block,
        count=1,
        flags=re.I | re.S,
    )
    block = re.sub(
        r'<div class="local-catalog-source">.*?</div>',
        f'<div class="premium-catalog-note"><strong>Giá & ưu đãi theo địa chỉ</strong><p>Mức hiển thị giúp so sánh nhanh. Khi đăng ký tại {escape(location)}, hệ thống sẽ kiểm tra hạ tầng, thiết bị và ưu đãi thực tế trước khi chốt.</p></div>',
        block,
        count=1,
        flags=re.I | re.S,
    )
    block = block.replace('data-full-plan-details="true"', 'data-full-plan-details="true" data-premium-catalog="v3"', 1)
    html = html[:section.start()] + block + html[section.end():]

    css = '<link rel="stylesheet" href="../../assets/css/local-catalog-premium.css" data-local-catalog-premium-style="v3"/>'
    js = '<script src="../../assets/js/local-catalog-premium.js" data-local-catalog-premium-script="v3" defer></script>'
    if 'data-local-catalog-premium-style=' not in html:
        html = html.replace('</head>', css + '</head>', 1)
    if 'data-local-catalog-premium-script=' not in html:
        html = html.replace('</body>', js + '</body>', 1)
    path.write_text(html, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    pages = sorted((Path(args.site) / 'khu-vuc').glob('*/index.html'))
    if len(pages) != 34:
        raise SystemExit(f"PREMIUM CATALOG BUILD FAIL: expected 34 province pages, got {len(pages)}")
    for page in pages:
        premiumize(page)
    print('PREMIUM CATALOG BUILT: 34/34 provinces × 56 premium package cards = 1904; legacy rich cards replaced; visible source links removed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
