from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

OLD_ORIGIN = "https://your-domain.example"
NEW_ORIGIN = "https://capquangfptminhlh.github.io/fpt"
SITE_BASE = "/fpt"
MOBILE_TAG = '<link rel="stylesheet" href="/fpt/assets/css/mobile-v3.css?v=20260817-4" data-mobile-v3="true"/>'

FORBIDDEN = (
    "your-domain.example",
    "url owner",
    "cannibalization",
    "seo intent",
    "source of truth",
    "kd/cpc",
    "fpt telecom demo",
    "fpt seo demo",
    "website demo",
    "bản coded demo",
    "local seo gate",
    "hold_local_evidence",
    "topical authority",
    "internal link",
    "seo owner",
    "intent informational",
    "intent giải trí",
    "money page",
    "faq chuẩn seo",
    "hỗ trợ seo",
)

TEXT_REPLACEMENTS = {
    "FPT Telecom Demo": "Tư vấn Internet FPT",
    "FPT SEO Demo": "Tư vấn Internet FPT",
    "FPT SEO demo": "Tư vấn Internet FPT",
    "Website demo độc lập, tổng hợp thông tin công khai để tư vấn chọn Internet FPT theo nhu cầu.":
        "Website tư vấn độc lập, tổng hợp thông tin công khai để hỗ trợ chọn Internet FPT theo nhu cầu.",
    "FPT Telecom – Demo giao diện mới cho website lắp mạng FPT, định hướng SEO hub + CRO + mobile-first.":
        "Thông tin tư vấn lắp mạng FPT, gói cước, WiFi, Camera và FPT Play theo nhu cầu thực tế.",
    "Website coded from approved demo concept.": "Website tư vấn Internet FPT.",
    "Bản coded demo đã thiết kế responsive hoàn chỉnh để bám theo ảnh demo desktop và mobile.":
        "Website được tối ưu responsive cho desktop, tablet và điện thoại.",
    "Dữ liệu form trong bản demo chưa kết nối CRM.": "",
    "SEO &amp; cấu trúc": "Thông tin bổ sung",
    "SEO & cấu trúc": "Thông tin bổ sung",
    "Vì sao trang này tách riêng?": "Câu hỏi thường gặp",
    "Trang owner cho transactional intent": "Đăng ký và tư vấn lắp đặt",
    "Trang danh mục &amp; use case": "Thông tin Internet theo nhu cầu",
    "Trang danh mục & use case": "Thông tin Internet theo nhu cầu",
    "Trang công nghệ &amp; phủ sóng": "Công nghệ và vùng phủ WiFi",
    "Trang công nghệ & phủ sóng": "Công nghệ và vùng phủ WiFi",
    "Trang entity cho từng gói": "So sánh và chọn gói Internet",
    "Trang FPT Play mô tả lợi ích combo internet + truyền hình, định vị rõ intent giải trí và nội dung đi kèm.":
        "FPT Play kết hợp Internet và truyền hình, tập trung trải nghiệm giải trí và nội dung đi kèm.",
    "Trang danh mục Internet FPT với bảng gói cước, trường hợp sử dụng, công nghệ WiFi và các route hỗ trợ SEO.":
        "Internet FPT với bảng gói cước, trường hợp sử dụng, công nghệ WiFi và các hướng dẫn liên quan.",
    "Trang SEO owner cho nhóm từ khóa cáp quang FPT, giải thích công nghệ FTTH và định hướng lựa chọn gói cước phù hợp.":
        "Tìm hiểu cáp quang FPT, công nghệ FTTH và cách lựa chọn gói cước phù hợp.",
    "Trang dịch vụ lắp mạng FPT với quy trình đăng ký, khu vực hỗ trợ, gói cước nổi bật và FAQ chuẩn SEO.":
        "Thông tin lắp mạng FPT với quy trình đăng ký, khu vực hỗ trợ, gói cước nổi bật và câu hỏi thường gặp.",
    "Tra cứu khu vực ở cấp tỉnh/thành, nhưng chỉ mở trang địa phương khi có bằng chứng local thật.":
        "Tra cứu khu vực lắp mạng FPT ở cấp tỉnh/thành và kiểm tra hạ tầng theo địa chỉ trước khi đăng ký.",
    "Nguồn/fact nhạy thời gian được kiểm tra ngày 15/08/2026; các nội dung biến động cần tái xác minh trước khi xuất bản thật.":
        "Thông tin có thể thay đổi theo thời điểm; dữ liệu về giá, ưu đãi và thiết bị nên được xác minh lại trước khi đăng ký.",
    "Trang tư vấn các dịch vụ Internet FPT, WiFi, Camera và FPT Play theo nhu cầu và khu vực.":
        "Website tư vấn độc lập về Internet FPT, WiFi, Camera và FPT Play theo nhu cầu và khu vực.",
    '<h1>WiFi mạnh ở <span>đúng nơi</span> bạn cần.</h1>':
        '<h1>Lắp mạng FPT — WiFi mạnh ở <span>đúng nơi</span> bạn cần.</h1>',
    "<td>Support</td>": "<td>Hỗ trợ</td>",
    "<td>Commercial</td>": "<td>Lựa chọn dịch vụ</td>",
    "<td>Informational</td>": "<td>Kiến thức</td>",
    "<td>Freshness</td>": "<td>Cập nhật mới</td>",
}


def prefix_project_paths(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        attr = match.group(1)
        path = match.group(2)
        if path.startswith("fpt/"):
            return match.group(0)
        return f'{attr}="{SITE_BASE}/{path}'

    return re.sub(r'\b(href|src)="/(?!/)([^"#]*)', repl, text)


def remove_internal_content(text: str) -> str:
    # Visible blocks that were useful during architecture work but should never be public-facing.
    text = re.sub(
        r'<h2[^>]*>\s*SEO intent và URL ownership\s*</h2>\s*<p>.*?</p>',
        '', text, flags=re.I | re.S,
    )
    text = re.sub(
        r'<h[23][^>]*>\s*SEO intent[^<]*</h[23]>\s*<p>.*?</p>',
        '', text, flags=re.I | re.S,
    )
    text = re.sub(
        r'<div class="fact-card"[^>]*>\s*<strong>\s*Source of truth\s*</strong>.*?</div>',
        '', text, flags=re.I | re.S,
    )
    text = re.sub(
        r'<div class="seo-box"[^>]*>.*?(?:URL owner|Canonical:|Mục tiêu:|cannibalization).*?</div>',
        '', text, flags=re.I | re.S,
    )
    text = re.sub(
        r'<figure[^>]*class="[^"]*demo-shot[^"]*"[^>]*>.*?</figure>',
        '', text, flags=re.I | re.S,
    )
    text = re.sub(
        r'<details[^>]*>\s*<summary>\s*(?:Trang này phục vụ intent gì\?|Website đã tối ưu mobile chưa\?)\s*</summary>.*?</details>',
        '', text, flags=re.I | re.S,
    )
    text = re.sub(
        r'<span>\s*(?:INFORMATIONAL|COMMERCIAL|TRANSACTIONAL|NAVIGATIONAL)\s*[·|]\s*[^<]+</span>',
        '', text, flags=re.I,
    )

    # Replace local-governance status with a user-facing availability note.
    text = re.sub(
        r'<div class="hold-local"[^>]*>.*?</div>',
        '<div class="hold-local"><strong>Kiểm tra theo địa chỉ:</strong> Khả năng triển khai, thiết bị và ưu đãi phụ thuộc hạ tầng thực tế. Vui lòng xác minh trước khi đăng ký.</div>',
        text, flags=re.I | re.S,
    )

    # Remove paragraphs/list items that expose editorial architecture instead of user value.
    text = re.sub(
        r'<p>[^<]*(?:URL owner|cannibalization|kiến trúc SEO hub|internal link)[^<]*</p>',
        '', text, flags=re.I,
    )
    text = re.sub(
        r'<li>[^<]*(?:Trang owner|URL owner|SEO với|SEO intent|intent [“"\']|intent chính|intent\s+(?:informational|commercial|transactional|navigational)|money page|internal link|topical authority|head term|hỗ trợ SEO)[^<]*</li>',
        '', text, flags=re.I,
    )

    # Remove structured-data blocks that contain internal governance language.
    def clean_schema(match: re.Match[str]) -> str:
        block = match.group(0)
        low = block.lower()
        if any(term in low for term in (
            "url owner", "cannibalization", "seo intent", "fpt seo demo", "fpt telecom demo",
            "local seo gate", "hold_local_evidence", "topical authority", "internal link",
        )):
            return ''
        return block

    text = re.sub(
        r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>',
        clean_schema, text, flags=re.I | re.S,
    )

    # Any leftover architecture badges are not useful to visitors.
    text = re.sub(r'\b(?:INFORMATIONAL|COMMERCIAL|TRANSACTIONAL|NAVIGATIONAL)\s*·\s*[A-Z-]+\b', '', text)
    text = re.sub(r'\s*Metrics volume/KD/CPC:\s*UNKNOWN\s*', '', text, flags=re.I)
    text = re.sub(r'<h3>\s*Câu hỏi thường gặp\s*</h3>\s*(?=<div class="faq")', '', text, flags=re.I)
    return text


def sanitize_html(text: str) -> str:
    text = text.replace(OLD_ORIGIN, NEW_ORIGIN)
    text = prefix_project_paths(text)

    for old, new in TEXT_REPLACEMENTS.items():
        text = text.replace(old, new)

    text = remove_internal_content(text)

    # Clean generic public-facing leftovers after targeted replacements.
    text = re.sub(r'(?i)\bFPT\s+SEO\s+demo\b', 'Tư vấn Internet FPT', text)
    text = re.sub(r'(?i)\bFPT\s+Telecom\s+Demo\b', 'Tư vấn Internet FPT', text)
    text = re.sub(r'(?i)\bWebsite\s+demo\b', 'Website', text)

    if 'data-mobile-v3=' not in text and '</head>' in text:
        text = text.replace('</head>', f'{MOBILE_TAG}</head>', 1)

    # Avoid empty artifacts created by block removal.
    text = re.sub(r'<p>\s*</p>', '', text)
    text = re.sub(r'<ul>\s*</ul>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


class AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.assets: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag in {"img", "script"} and data.get("src"):
            self.assets.append((tag, data["src"] or ""))
        elif tag == "link" and data.get("href"):
            rel = (data.get("rel") or "").lower()
            if any(kind in rel for kind in ("stylesheet", "icon", "preload")):
                self.assets.append((tag, data["href"] or ""))


def local_asset_target(site: Path, html_file: Path, ref: str) -> Path | None:
    ref = ref.strip()
    if not ref or ref.startswith(("http://", "https://", "data:", "mailto:", "tel:", "javascript:", "#")):
        return None

    split = urlsplit(ref)
    path = split.path
    if not path:
        return None

    if path.startswith(f"{SITE_BASE}/"):
        return site / path[len(SITE_BASE) + 1:]
    if path == SITE_BASE:
        return site / "index.html"
    if path.startswith('/'):
        return site / path[1:]
    return (html_file.parent / path).resolve()


def run_qa(site: Path) -> None:
    html_files = sorted(site.rglob('*.html'))
    if len(html_files) < 70:
        raise SystemExit(f"QA FAIL: expected at least 70 HTML pages, found {len(html_files)}")

    seo_images = list((site / 'assets' / 'images' / 'seo').glob('*.webp'))
    if len(seo_images) < 100:
        raise SystemExit(f"QA FAIL: SEO images missing from production artifact; found only {len(seo_images)}")

    forbidden_hits: list[str] = []
    missing_assets: list[str] = []

    site_resolved = site.resolve()
    for html_file in html_files:
        text = html_file.read_text(encoding='utf-8')
        low = text.lower()
        for term in FORBIDDEN:
            if term in low:
                forbidden_hits.append(f"{html_file.relative_to(site)} :: {term}")

        parser = AssetParser()
        parser.feed(text)
        for tag, ref in parser.assets:
            target = local_asset_target(site, html_file, ref)
            if target is None:
                continue
            try:
                target_resolved = target.resolve()
                target_resolved.relative_to(site_resolved)
            except (ValueError, OSError):
                missing_assets.append(f"{html_file.relative_to(site)} :: {tag} {ref} (outside site root)")
                continue
            if not target_resolved.exists():
                missing_assets.append(f"{html_file.relative_to(site)} :: {tag} {ref}")

    if forbidden_hits:
        preview = '\n'.join(forbidden_hits[:30])
        raise SystemExit(f"QA FAIL: internal/demo text leaked to production:\n{preview}")

    if missing_assets:
        preview = '\n'.join(missing_assets[:50])
        raise SystemExit(f"QA FAIL: missing local assets:\n{preview}")

    print(
        f"QA PASS: {len(html_files)} HTML pages, {len(seo_images)} SEO images, "
        "0 forbidden internal phrases, 0 missing local assets"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', default='_site')
    args = parser.parse_args()
    site = Path(args.site)

    if not site.exists():
        print(f"Site directory not found: {site}", file=sys.stderr)
        return 2

    for html_file in site.rglob('*.html'):
        original = html_file.read_text(encoding='utf-8')
        html_file.write_text(sanitize_html(original), encoding='utf-8')

    # XML/TXT still need canonical origin replacement.
    for path in list(site.rglob('*.xml')) + list(site.rglob('*.txt')):
        text = path.read_text(encoding='utf-8')
        path.write_text(text.replace(OLD_ORIGIN, NEW_ORIGIN), encoding='utf-8')

    (site / 'robots.txt').write_text(
        'User-agent: *\nAllow: /fpt/\nSitemap: https://capquangfptminhlh.github.io/fpt/sitemap.xml\n',
        encoding='utf-8',
    )
    (site / '.nojekyll').touch()

    run_qa(site)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
