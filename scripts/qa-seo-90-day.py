from __future__ import annotations

import argparse
import re
from collections import Counter
from html import unescape
from pathlib import Path

ORIGIN = "https://capquangfptminhlh.github.io/fpt"

CORE_ROUTES = (
    "index.html",
    "lap-mang-fpt/index.html",
    "internet-fpt/index.html",
    "cap-quang-fpt/index.html",
    "goi-cuoc-fpt/index.html",
    "bang-gia-fpt/index.html",
    "wifi-fpt/index.html",
    "wifi-6-fpt/index.html",
    "wifi-7/index.html",
    "xgs-pon-fpt/index.html",
    "speedx-fpt/index.html",
    "f-game-fpt/index.html",
    "fpt-play/index.html",
    "camera-fpt/index.html",
    "combo-fpt/index.html",
    "khu-vuc/index.html",
    "so-sanh/index.html",
    "ho-tro/index.html",
    "kien-thuc/index.html",
)

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
DESC_RE = re.compile(r'<meta\b(?=[^>]*\bname=["\']description["\'])(?=[^>]*\bcontent=["\']([^"\']+)["\'])[^>]*>', re.I | re.S)
CANON_RE = re.compile(r'<link\b(?=[^>]*\brel=["\']canonical["\'])(?=[^>]*\bhref=["\']([^"\']+)["\'])[^>]*>', re.I | re.S)
ROBOTS_RE = re.compile(r'<meta\b(?=[^>]*\bname=["\']robots["\'])(?=[^>]*\bcontent=["\']([^"\']+)["\'])[^>]*>', re.I | re.S)
H1_RE = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.I | re.S)
A_RE = re.compile(r'<a\b[^>]*\bhref=["\']([^"\']+)["\'][^>]*>', re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(TAG_RE.sub(" ", value))).strip()


def one(pattern: re.Pattern[str], text: str) -> str:
    match = pattern.search(text)
    return clean(match.group(1)) if match else ""


def noindex(text: str) -> bool:
    value = one(ROBOTS_RE, text).lower()
    return "noindex" in value


def is_internal(href: str) -> bool:
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return False
    if href.startswith(("http://", "https://")):
        return href.startswith(ORIGIN + "/") or href == ORIGIN
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True)
    args = parser.parse_args()
    site = Path(args.site)

    errors: list[str] = []
    for rel in CORE_ROUTES:
        path = site / rel
        if not path.exists():
            errors.append(f"core route missing: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        if noindex(text):
            errors.append(f"core route is noindex: {rel}")

    indexable: list[tuple[Path, str]] = []
    for path in sorted(site.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        if not noindex(text):
            indexable.append((path, text))

    if len(indexable) < 106:
        errors.append(f"expected at least 106 indexable pages, found {len(indexable)}")

    titles: Counter[str] = Counter()
    canonicals: Counter[str] = Counter()
    internal_links = 0
    orphan_risk: list[str] = []

    for path, text in indexable:
        rel = path.relative_to(site).as_posix()
        title = one(TITLE_RE, text)
        desc = one(DESC_RE, text)
        canonical = one(CANON_RE, text)
        h1 = one(H1_RE, text)

        if not title:
            errors.append(f"{rel}: missing title")
        else:
            titles[title] += 1
        if not desc:
            errors.append(f"{rel}: missing meta description")
        if not canonical:
            errors.append(f"{rel}: missing canonical")
        else:
            canonicals[canonical] += 1
            if not canonical.startswith(ORIGIN + "/"):
                errors.append(f"{rel}: canonical outside production origin: {canonical}")
        if not h1:
            errors.append(f"{rel}: missing H1")

        links = [href for href in A_RE.findall(text) if is_internal(href)]
        internal_links += len(links)
        if len(links) < 3:
            orphan_risk.append(f"{rel} ({len(links)} internal links)")

    duplicate_titles = [title for title, count in titles.items() if count > 1]
    duplicate_canonicals = [url for url, count in canonicals.items() if count > 1]
    if duplicate_titles:
        errors.append("duplicate indexable titles: " + " | ".join(duplicate_titles[:10]))
    if duplicate_canonicals:
        errors.append("duplicate canonicals: " + " | ".join(duplicate_canonicals[:10]))
    if orphan_risk:
        errors.append("indexable pages with <3 crawlable internal links: " + ", ".join(orphan_risk[:10]))
    if internal_links < 4500:
        errors.append(f"internal-link graph regressed: {internal_links} < 4500")

    homepage = (site / "index.html").read_text(encoding="utf-8")
    if '"@type":"WebSite"' not in homepage and '"@type": "WebSite"' not in homepage:
        errors.append("homepage missing WebSite structured data")

    local_pages = sorted((site / "khu-vuc").glob("*/index.html"))
    if len(local_pages) != 34:
        errors.append(f"expected 34 local landing pages, found {len(local_pages)}")
    premium_offers = 0
    editorial_pages = 0
    for path in local_pages:
        text = path.read_text(encoding="utf-8")
        count = text.count("data-premium-plan-card")
        premium_offers += count
        if count < 103:
            errors.append(f"{path.parent.name}: premium offer count {count} < 103")
        if "data-local-editorial-v2" in text:
            editorial_pages += 1
        elif "local-editorial-v2" in text:
            editorial_pages += 1
        else:
            # Fall back to structural proof if the exact marker changes.
            if text.count("<h2") >= 13 and len(clean(text).split()) >= 2200:
                editorial_pages += 1
            else:
                errors.append(f"{path.parent.name}: longform local editorial proof missing")

    if premium_offers < 3502:
        errors.append(f"premium local offer inventory regressed: {premium_offers} < 3502")
    if editorial_pages != 34:
        errors.append(f"local editorial depth regressed: {editorial_pages}/34")

    robots = (site / "robots.txt").read_text(encoding="utf-8") if (site / "robots.txt").exists() else ""
    if f"Sitemap: {ORIGIN}/sitemap.xml" not in robots:
        errors.append("robots.txt missing production sitemap declaration")

    if errors:
        raise SystemExit("SEO 90-DAY QA FAIL:\n- " + "\n- ".join(errors))

    print(
        "SEO 90-DAY QA PASS: "
        f"indexable={len(indexable)}, core_routes={len(CORE_ROUTES)}, "
        f"internal_links={internal_links}, local_editorial={editorial_pages}/34, "
        f"premium_offers={premium_offers}, unique_titles={len(titles)}, unique_canonicals={len(canonicals)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
