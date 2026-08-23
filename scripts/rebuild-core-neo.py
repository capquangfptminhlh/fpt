from __future__ import annotations

import argparse
import re
from pathlib import Path

STYLE = '<link rel="stylesheet" href="/fpt/assets/css/core-neo.css?v=20260823-1" data-core-neo-style="true"/>'

PAGES = {
    'internet-fpt/index.html': {
        'kicker': 'Internet FPT',
        'title': 'Internet mạnh cho mọi góc nhà.',
        'desc': 'Chọn đường truyền theo số thiết bị, diện tích, số tầng và cách gia đình thực sự sử dụng Internet mỗi ngày.',
        'image': '/fpt/assets/images/hero-family.webp',
        'float': ('Đến 1 Gbps', 'Tốc độ cao · nhiều thiết bị'),
        'cards': [
            ('Gói cước', 'GIGA · SKY · META', 'So sánh tốc độ và nhu cầu để chọn đúng gói.', '/fpt/goi-cuoc-fpt/'),
            ('Công nghệ', 'WiFi 7 & Mesh', 'Tối ưu vùng phủ thay vì chỉ nhìn con số Mbps.', '/fpt/wifi-7/'),
            ('Kiểm tra', 'Hạ tầng theo địa chỉ', 'Xác nhận khả năng triển khai trước khi đăng ký.', '/fpt/lien-he/'),
        ],
    },
    'goi-cuoc-fpt/index.html': {
        'kicker': 'Gói cước FPT',
        'title': 'Chọn gói theo cách bạn sử dụng.',
        'desc': 'GIGA, SKY, META và các nhóm combo được trình bày theo nhu cầu thực tế: thiết bị, upload, game, camera và nhiều tầng.',
        'image': '/fpt/assets/images/seo/goi-cuoc-fpt-hero.webp',
        'float': ('GIGA · SKY · META', 'So sánh nhanh · chọn dễ hơn'),
        'cards': [
            ('Cơ bản', 'GIGA', 'Phù hợp gia đình nhỏ và nhu cầu hằng ngày.', '/fpt/goi-cuoc/giga/'),
            ('Cân bằng', 'SKY', 'Nhiều thiết bị, download cao và giải trí 4K.', '/fpt/goi-cuoc/sky/'),
            ('Hiệu năng', 'META', 'Upload cao cho cloud, camera và công việc nặng.', '/fpt/goi-cuoc/meta/'),
        ],
    },
    'combo-fpt/index.html': {
        'kicker': 'Combo FPT',
        'title': 'Internet và giải trí trong một trải nghiệm.',
        'desc': 'Kết hợp Internet FPT với FPT Play để cả nhà dùng mạng, xem nội dung và giải trí trên nhiều màn hình thuận tiện hơn.',
        'image': '/fpt/assets/images/promo-fptplay.webp',
        'float': ('Internet + Play', 'Một đăng ký · nhiều trải nghiệm'),
        'cards': [
            ('Internet', 'Đường truyền mạnh', 'Nền tảng ổn định cho mọi thiết bị trong nhà.', '/fpt/internet-fpt/'),
            ('Giải trí', 'FPT Play', 'Nội dung trên TV, điện thoại và máy tính bảng.', '/fpt/fpt-play/'),
            ('Tư vấn', 'Chọn combo phù hợp', 'Kiểm tra gói khả dụng theo địa chỉ thực tế.', '/fpt/lien-he/'),
        ],
    },
    'wifi-7/index.html': {
        'kicker': 'WiFi 7 FPT',
        'title': 'WiFi nhanh phải mạnh ở nơi bạn cần.',
        'desc': 'WiFi 7 hướng tới không gian nhiều thiết bị, độ trễ thấp và nhu cầu băng thông cao; vùng phủ thực tế vẫn phụ thuộc bố trí nhà.',
        'image': '/fpt/assets/images/promo-wifi7.webp',
        'float': ('WiFi 7', 'Độ trễ thấp · nhiều thiết bị'),
        'cards': [
            ('Hiệu năng', 'Nhiều thiết bị hơn', 'Tối ưu cho gia đình hiện đại và smart home.', '/fpt/wifi-7/'),
            ('Vùng phủ', 'Mesh WiFi', 'Mở rộng tín hiệu cho nhà nhiều phòng hoặc nhiều tầng.', '/fpt/mesh-wifi-fpt/'),
            ('Đường truyền', 'XGS-PON', 'Kết hợp hạ tầng mạnh với WiFi thế hệ mới.', '/fpt/xgs-pon-fpt/'),
        ],
    },
    'camera-fpt/index.html': {
        'kicker': 'FPT Camera',
        'title': 'Quan sát ngôi nhà. Mọi lúc, mọi nơi.',
        'desc': 'Camera kết hợp Internet ổn định để theo dõi từ xa, lưu trữ cloud và duy trì kết nối cho nhiều điểm quan sát.',
        'image': '/fpt/assets/images/promo-camera.webp',
        'float': ('24/7', 'Quan sát · kết nối · lưu trữ'),
        'cards': [
            ('Quan sát', 'Xem từ xa', 'Theo dõi không gian qua thiết bị cá nhân.', '/fpt/camera-fpt/'),
            ('Lưu trữ', 'Cloud', 'Giảm phụ thuộc vào lưu trữ cục bộ tại nhà.', '/fpt/camera-fpt/'),
            ('Kết nối', 'Internet ổn định', 'Nhiều camera cần quan tâm cả upload và WiFi.', '/fpt/internet-fpt/'),
        ],
    },
    'fpt-play/index.html': {
        'kicker': 'FPT Play',
        'title': 'Giải trí trên mọi màn hình.',
        'desc': 'Kết hợp truyền hình, thể thao, phim và nội dung giải trí với đường truyền Internet ổn định cho cả gia đình.',
        'image': '/fpt/assets/images/promo-fptplay.webp',
        'float': ('FPT Play', 'TV · điện thoại · tablet'),
        'cards': [
            ('Nội dung', 'Giải trí đa dạng', 'Khám phá nội dung trên nhiều nhóm thiết bị.', '/fpt/fpt-play/'),
            ('Kết hợp', 'Combo Internet', 'Một lựa chọn gọn cho kết nối và giải trí.', '/fpt/combo-fpt/'),
            ('Đường truyền', 'Xem ổn định hơn', 'Chọn tốc độ và WiFi phù hợp số màn hình sử dụng.', '/fpt/internet-fpt/'),
        ],
    },
    'khu-vuc/index.html': {
        'kicker': 'Khu vực lắp đặt',
        'title': 'Kiểm tra hạ tầng theo đúng địa chỉ.',
        'desc': 'Khả năng triển khai, thiết bị và ưu đãi có thể khác nhau theo khu vực. Chọn tỉnh/thành rồi xác minh địa chỉ trước khi chốt.',
        'image': '/fpt/assets/images/seo/khu-vuc-hero.webp',
        'float': ('34 tỉnh/thành', 'Tra cứu · kiểm tra · xác nhận'),
        'cards': [
            ('Tra cứu', 'Chọn tỉnh/thành', 'Đi tới đúng khu vực đang cần lắp đặt.', '/fpt/khu-vuc/'),
            ('Xác minh', 'Theo địa chỉ', 'Hạ tầng thực tế được kiểm tra trước khi đăng ký.', '/fpt/lien-he/'),
            ('Tham khảo', 'Gói cước', 'So sánh trước rồi xác nhận gói khả dụng tại địa chỉ.', '/fpt/goi-cuoc-fpt/'),
        ],
    },
    'ho-tro/index.html': {
        'kicker': 'Hỗ trợ FPT',
        'title': 'Cần hỗ trợ? Đi thẳng vào vấn đề.',
        'desc': 'Từ lắp đặt, WiFi yếu, mật khẩu, tốc độ đến tư vấn gói: tìm hướng dẫn phù hợp hoặc liên hệ để được hỗ trợ nhanh.',
        'image': '/fpt/assets/images/seo/ho-tro-hero.webp',
        'float': ('24/7', 'Hỗ trợ kỹ thuật · 1900 6600'),
        'cards': [
            ('Lắp đặt', 'Trước khi lắp', 'Thời gian, phí và các bước cần chuẩn bị.', '/fpt/ho-tro/lap-mang-fpt-mat-bao-lau/'),
            ('WiFi', 'Xử lý kết nối', 'Kiểm tra khi WiFi yếu hoặc cần đổi mật khẩu.', '/fpt/ho-tro/wifi-fpt-yeu/'),
            ('Liên hệ', 'Cần người hỗ trợ', 'Gửi yêu cầu để được tư vấn theo tình huống thực tế.', '/fpt/lien-he/'),
        ],
    },
}


def add_body_class(html: str) -> str:
    match = re.search(r'<body\b([^>]*)>', html, flags=re.I)
    if not match:
        raise ValueError('missing body')
    attrs = match.group(1)
    class_match = re.search(r'class=["\']([^"\']*)["\']', attrs, flags=re.I)
    if class_match:
        classes = class_match.group(1).split()
        if 'neo-core-page' not in classes:
            classes.append('neo-core-page')
        attrs = re.sub(r'class=["\'][^"\']*["\']', f'class="{" ".join(classes)}"', attrs, count=1, flags=re.I)
    else:
        attrs += ' class="neo-core-page"'
    return html[:match.start()] + f'<body{attrs}>' + html[match.end():]


def strip_first_hero(main_inner: str) -> str:
    # Core menu pages use either seo-hero or subpage-hero. They do not nest section tags.
    return re.sub(
        r'<section\b[^>]*class=["\'][^"\']*(?:seo-hero|subpage-hero)[^"\']*["\'][^>]*>.*?</section>',
        '', main_inner, count=1, flags=re.I | re.S,
    )


def hero(config: dict[str, object]) -> str:
    float_title, float_sub = config['float']
    return f'''<section class="core-neo-hero" data-core-neo-hero="true">
<div class="container core-neo-grid">
  <div>
    <span class="core-neo-kicker">{config['kicker']}</span>
    <h1>{config['title']}</h1>
    <p>{config['desc']}</p>
    <div class="core-neo-actions">
      <a class="core-neo-btn primary" href="/fpt/lien-he/">Kiểm tra &amp; đăng ký</a>
      <a class="core-neo-btn secondary" href="/fpt/goi-cuoc-fpt/">Xem gói cước</a>
    </div>
    <div class="core-neo-proof"><span><i>✓</i> Tone Neo đồng nhất</span><span><i>✓</i> Hỗ trợ 24/7</span><span><i>✓</i> Responsive mobile</span></div>
  </div>
  <div class="core-neo-visual">
    <div class="core-neo-photo"><img src="{config['image']}" alt="{config['kicker']}" fetchpriority="high"/></div>
    <div class="core-neo-float"><b>{float_title}</b><span>{float_sub}</span></div>
  </div>
</div>
</section>'''


def cards(config: dict[str, object]) -> str:
    chunks = []
    for index, (small, title, desc, href) in enumerate(config['cards']):
        dark = ' dark' if index == 1 else ''
        chunks.append(
            f'<a class="core-neo-card{dark}" href="{href}"><small>{small}</small><h2>{title}</h2><p>{desc}</p><strong>Khám phá →</strong></a>'
        )
    return '<section class="core-neo-overlap"><div class="container core-neo-cards">' + ''.join(chunks) + '</div></section>'


def cta() -> str:
    return '''<section class="core-neo-cta"><div class="container core-neo-cta-box"><div><h2>Chọn đúng trước khi đăng ký.</h2><p>Kiểm tra địa chỉ, nhu cầu sử dụng và thiết bị để nhận tư vấn phù hợp thay vì chỉ chọn theo một con số tốc độ.</p></div><div class="core-neo-cta-actions"><a class="core-neo-btn primary" href="/fpt/lien-he/">Kiểm tra hạ tầng</a><a class="core-neo-btn secondary" href="tel:19006600">Gọi 1900 6600</a></div></div></section>'''


def rebuild(html: str, config: dict[str, object]) -> str:
    if 'data-core-neo-style=' not in html:
        html = html.replace('</head>', STYLE + '</head>', 1)
    html = add_body_class(html)
    main_match = re.search(r'<main\b[^>]*>(.*?)</main>', html, flags=re.I | re.S)
    if not main_match:
        raise ValueError('missing main')
    legacy = strip_first_hero(main_match.group(1)).strip()
    new_main = '<main>' + hero(config) + cards(config) + '<div class="core-neo-content">' + legacy + '</div>' + cta() + '</main>'
    return html[:main_match.start()] + new_main + html[main_match.end():]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    args = parser.parse_args()
    site = Path(args.site)
    errors: list[str] = []
    changed = 0

    for rel, config in PAGES.items():
        path = site / rel
        if not path.exists():
            errors.append(f'missing core page: {rel}')
            continue
        old = path.read_text(encoding='utf-8')
        try:
            new = rebuild(old, config)
        except ValueError as exc:
            errors.append(f'{rel}: {exc}')
            continue
        path.write_text(new, encoding='utf-8')
        changed += 1

    css = site / 'assets/css/core-neo.css'
    if not css.exists():
        errors.append('missing assets/css/core-neo.css')

    if errors:
        print('CORE NEO REBUILD FAIL')
        for error in errors:
            print(f'- {error}')
        raise SystemExit(1)

    print(f'CORE NEO REBUILD PASS: pages={changed}, shared_layout=neo, legacy_content=preserved')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
