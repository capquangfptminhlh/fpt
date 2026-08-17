from __future__ import annotations

import argparse
import json
import re
from html import unescape
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree

ORIGIN = "https://capquangfptminhlh.github.io/fpt"
ADMIN_SOURCE_HOST = "xaydungchinhsach.chinhphu.vn"
FPT_SOURCE_HOST = "fpt.vn"

ROBOTS_META = re.compile(
    r'<meta\b(?=[^>]*\bname=["\']robots["\'])(?=[^>]*\bcontent=["\']([^"\']+)["\'])[^>]*>',
    flags=re.I | re.S,
)
TITLE_RE = re.compile(r'<title>(.*?)</title>', flags=re.I | re.S)
DESC_RE = re.compile(
    r'<meta\b(?=[^>]*\bname=["\']description["\'])(?=[^>]*\bcontent=["\']([^"\']*)["\'])[^>]*>',
    flags=re.I | re.S,
)
CANONICAL_RE = re.compile(
    r'<link\b(?=[^>]*\brel=["\']canonical["\'])(?=[^>]*\bhref=["\']([^"\']+)["\'])[^>]*>',
    flags=re.I | re.S,
)
H1_RE = re.compile(r'<h1\b[^>]*>(.*?)</h1>', flags=re.I | re.S)
JSONLD_RE = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    flags=re.I | re.S,
)
TAG_RE = re.compile(r'<[^>]+>')


def clean(value: str) -> str:
    return re.sub(r'\s+', ' ', unescape(TAG_RE.sub('', value))).strip()


def expected_url(relative: Path) -> str:
    parts = relative.parts
    if parts[-1] == "index.html":
        path = "/".join(parts[:-1])
        return f"{ORIGIN}/{path}/" if path else f"{ORIGIN}/"
    return f"{ORIGIN}/" + "/".join(parts)


def robots(text: str) -> str:
    match = ROBOTS_META.search(text)
    return match.group(1).lower() if match else ""


def is_noindex(text: str) -> bool:
    return "noindex" in robots(text)


def one(pattern: re.Pattern[str], text: str, label: str, rel: Path, errors: list[str]) -> str:
    matches = pattern.findall(text)
    if len(matches) != 1:
        errors.append(f"{rel}: expected exactly one {label}, found {len(matches)}")
        return ""
    return clean(matches[0])


def schema_objects(text: str, rel: Path, errors: list[str]) -> list[dict]:
    objects: list[dict] = []
    for idx, raw in enumerate(JSONLD_RE.findall(text), start=1):
        raw = raw.strip()
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{rel}: invalid JSON-LD block {idx}: {exc}")
            continue
        if isinstance(parsed, dict):
            objects.append(parsed)
        elif isinstance(parsed, list):
            objects.extend(x for x in parsed if isinstance(x, dict))
    return objects


def walk_schema(obj):
    if isinstance(obj, dict):
        yield obj
        graph = obj.get("@graph")
        if isinstance(graph, list):
            for item in graph:
                yield from walk_schema(item)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk_schema(item)


def schema_types(objects: list[dict]) -> set[str]:
    types: set[str] = set()
    for root in objects:
        for obj in walk_schema(root):
            value = obj.get("@type")
            if isinstance(value, str):
                types.add(value)
            elif isinstance(value, list):
                types.update(x for x in value if isinstance(x, str))
    return types


def service_area(objects: list[dict]) -> tuple[str, str] | None:
    for root in objects:
        for obj in walk_schema(root):
            value = obj.get("@type")
            is_service = value == "Service" or (isinstance(value, list) and "Service" in value)
            if not is_service:
                continue
            area = obj.get("areaServed")
            if isinstance(area, dict):
                return str(area.get("@type", "")), str(area.get("name", ""))
    return None


def sitemap_urls(path: Path) -> set[str]:
    root = ElementTree.parse(path).getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return {
        (node.text or "").strip()
        for node in root.findall("s:url/s:loc", ns)
        if (node.text or "").strip()
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True)
    args = parser.parse_args()
    site = Path(args.site)
    sitemap_path = site / "sitemap.xml"
    robots_path = site / "robots.txt"
    if not sitemap_path.exists():
        raise SystemExit("SEARCH QUALITY QA FAIL: sitemap.xml missing")
    if not robots_path.exists():
        raise SystemExit("SEARCH QUALITY QA FAIL: robots.txt missing")

    errors: list[str] = []
    warnings: list[str] = []
    sitemap = sitemap_urls(sitemap_path)
    indexable_urls: set[str] = set()
    noindex_urls: set[str] = set()
    canonical_owner: dict[str, Path] = {}
    local_landings = 0
    empty_news = 0
    jsonld_blocks = 0

    html_files = sorted(site.rglob("*.html"))
    for path in html_files:
        rel = path.relative_to(site)
        text = path.read_text(encoding="utf-8")
        if not re.search(r'<html\b[^>]*\blang=["\']vi(?:-VN)?["\']', text, flags=re.I):
            errors.append(f"{rel}: html lang must be vi or vi-VN")

        title = one(TITLE_RE, text, "title", rel, errors)
        description = one(DESC_RE, text, "meta description", rel, errors)
        canonical = one(CANONICAL_RE, text, "canonical", rel, errors)
        h1_matches = H1_RE.findall(text)

        schemas = schema_objects(text, rel, errors)
        jsonld_blocks += len(JSONLD_RE.findall(text))

        page_url = expected_url(rel)
        noindex = is_noindex(text)
        if noindex:
            noindex_urls.add(page_url)
        else:
            indexable_urls.add(page_url)
            if not h1_matches:
                errors.append(f"{rel}: indexable page missing H1")
            if not title:
                errors.append(f"{rel}: indexable page has empty title")
            if not description:
                errors.append(f"{rel}: indexable page has empty meta description")
            if not canonical:
                errors.append(f"{rel}: indexable page missing canonical")
            elif canonical != page_url:
                errors.append(f"{rel}: canonical mismatch {canonical} != {page_url}")
            if canonical:
                previous = canonical_owner.get(canonical)
                if previous is not None and previous != rel:
                    errors.append(f"{rel}: duplicate canonical also used by {previous}: {canonical}")
                canonical_owner[canonical] = rel

        if canonical:
            split = urlsplit(canonical)
            if split.scheme != "https" or not canonical.startswith(ORIGIN + "/"):
                errors.append(f"{rel}: canonical must be HTTPS under production origin: {canonical}")

        if len(rel.parts) == 3 and rel.parts[0] == "khu-vuc" and rel.parts[2] == "index.html":
            local_landings += 1
            if noindex:
                errors.append(f"{rel}: local service landing must be indexable")
            if "max-image-preview:large" not in robots(text):
                errors.append(f"{rel}: local landing robots meta missing max-image-preview:large")
            if "Kiểm tra theo địa chỉ" not in clean(text):
                errors.append(f"{rel}: local landing missing answer-first address verification guidance")
            if text.count("<details") < 4:
                errors.append(f"{rel}: local landing should expose at least 4 visible Q&A blocks")
            types = schema_types(schemas)
            if "Service" not in types or "BreadcrumbList" not in types:
                errors.append(f"{rel}: local landing requires Service + BreadcrumbList JSON-LD")
            area = service_area(schemas)
            if not area or area[0] != "AdministrativeArea" or not area[1]:
                errors.append(f"{rel}: Service.areaServed must be AdministrativeArea with a name")
            else:
                h1_text = clean(h1_matches[0]) if h1_matches else ""
                if area[1].lower() not in h1_text.lower():
                    errors.append(f"{rel}: areaServed name must match visible H1 location")
            if ADMIN_SOURCE_HOST not in text or FPT_SOURCE_HOST not in text:
                errors.append(f"{rel}: local landing missing visible government/FPT evidence links")
            if canonical not in sitemap:
                errors.append(f"{rel}: indexable local landing missing from sitemap")

        if len(rel.parts) == 4 and rel.parts[0] == "khu-vuc" and rel.parts[2] == "tin-tuc" and rel.parts[3] == "index.html":
            empty_news += 1
            if 'data-local-news-status="empty"' not in text:
                errors.append(f"{rel}: local news hub missing explicit empty status marker")
            directives = robots(text)
            if "noindex" not in directives or "follow" not in directives:
                errors.append(f"{rel}: empty local news hub must be noindex,follow")
            if page_url in sitemap or (canonical and canonical in sitemap):
                errors.append(f"{rel}: noindex local news hub leaked into sitemap")
            types = schema_types(schemas)
            if "CollectionPage" not in types or "BreadcrumbList" not in types:
                errors.append(f"{rel}: local news hub requires CollectionPage + BreadcrumbList JSON-LD")
            if "Tin địa phương chỉ xuất bản khi có nguồn." not in text:
                errors.append(f"{rel}: local news hub missing visible evidence policy")

    missing = sorted(indexable_urls - sitemap)
    leaked = sorted(sitemap - indexable_urls)
    if missing:
        errors.append("sitemap missing indexable URLs: " + ", ".join(missing[:10]))
    if leaked:
        errors.append("sitemap contains non-indexable/unknown URLs: " + ", ".join(leaked[:10]))

    if local_landings != 34:
        errors.append(f"expected 34 local landings, found {local_landings}")
    if empty_news != 34:
        errors.append(f"expected 34 empty local news hubs, found {empty_news}")

    robots_text = robots_path.read_text(encoding="utf-8")
    expected_sitemap = f"Sitemap: {ORIGIN}/sitemap.xml"
    if expected_sitemap not in robots_text:
        errors.append("robots.txt missing production sitemap declaration")

    warnings.append(
        "GitHub project Pages serves robots.txt under /fpt/; host-root robots control requires "
        "a custom domain or root github.io site."
    )

    if errors:
        raise SystemExit("SEARCH QUALITY QA FAIL:\n- " + "\n- ".join(errors))

    print(
        f"SEARCH QUALITY QA PASS: html={len(html_files)}, indexable={len(indexable_urls)}, "
        f"noindex={len(noindex_urls)}, sitemap={len(sitemap)}, jsonld_blocks={jsonld_blocks}, "
        f"local_geo={local_landings}/34, empty_news_noindex={empty_news}/34"
    )
    for warning in warnings:
        print("SEARCH QUALITY NOTE:", warning)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
