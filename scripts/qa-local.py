from __future__ import annotations

import argparse
import csv
import json
import re
from html.parser import HTMLParser
from pathlib import Path

SITE_ORIGIN = "https://capquangfptminhlh.github.io/fpt"
BAD_SLUGS = ("/khu-vuc/a-nang/", "/khu-vuc/ak-lak/", "/khu-vuc/ien-bien/", "/khu-vuc/ong-nai/", "/khu-vuc/ong-thap/")
FORBIDDEN_CLAIMS = ("phủ sóng 100%", "lắp được mọi địa chỉ", "cam kết lắp trong", "giá áp dụng toàn tỉnh", "khuyến mãi áp dụng toàn tỉnh")


class MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(); self.title=""; self._in_title=False; self.h1=[]; self._in_h1=False; self.desc=""; self.canonical=""
    def handle_starttag(self, tag, attrs):
        data=dict(attrs)
        if tag=="title": self._in_title=True
        elif tag=="h1": self._in_h1=True
        elif tag=="meta" and data.get("name")=="description": self.desc=data.get("content","")
        elif tag=="link" and data.get("rel")=="canonical": self.canonical=data.get("href","")
    def handle_endtag(self, tag):
        if tag=="title": self._in_title=False
        elif tag=="h1": self._in_h1=False
    def handle_data(self, data):
        if self._in_title: self.title += data
        if self._in_h1: self.h1.append(data)


def word_count(text: str) -> int:
    visible=re.sub(r"<script\b.*?</script>"," ",text,flags=re.I|re.S); visible=re.sub(r"<style\b.*?</style>"," ",visible,flags=re.I|re.S); visible=re.sub(r"<[^>]+>"," ",visible)
    return len(re.findall(r"\b[\wÀ-ỹ]+\b",visible,flags=re.UNICODE))


def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument("--site",required=True); args=ap.parse_args()
    root=Path(__file__).resolve().parents[1]; site=Path(args.site); data=json.loads((root/"data"/"local-provinces.json").read_text(encoding="utf-8")); provinces=data["provinces"]; errors=[]
    if len(provinces)!=34: errors.append(f"province config must have 34 rows, got {len(provinces)}")
    slugs=[p["slug"] for p in provinces]; codes=[p["code"] for p in provinces]
    if len(set(slugs))!=34: errors.append("province slugs are not unique")
    if len(set(codes))!=34: errors.append("province codes are not unique")
    predecessor_names={name for p in provinces for name in p["merged_from"]}
    if len(predecessor_names)!=63: errors.append(f"merged_from should cover 63 provincial unit names before the June-2025 consolidation, got {len(predecessor_names)}")

    keyword_path=root/"seo"/"local-keyword-map.csv"
    with keyword_path.open(encoding="utf-8-sig",newline="") as fh: rows=list(csv.DictReader(fh))
    if len(rows)<3500: errors.append(f"expected >=3500 local keyword rows, got {len(rows)}")
    urls={f"/khu-vuc/{p['slug']}/" for p in provinces}; keyword_urls={r["proposed_url"] for r in rows}
    if not urls.issubset(keyword_urls): errors.append("keyword map does not cover all 34 canonical local URLs")
    for p in provinces:
        target=f"/khu-vuc/{p['slug']}/"; page_rows=[r for r in rows if r["proposed_url"]==target]
        if len(page_rows)<50: errors.append(f"{p['slug']}: only {len(page_rows)} keyword rows")
        for alias in p["aliases"]:
            if not any(r["location"]==alias and r["proposed_url"]==target for r in page_rows): errors.append(f"{p['slug']}: alias missing from keyword map: {alias}")

    local_pages=[]; titles=set(); descs=set(); h1s=set(); index_text=(site/"khu-vuc"/"index.html").read_text(encoding="utf-8")
    for p in provinces:
        page=site/"khu-vuc"/p["slug"] / "index.html"
        if not page.exists(): errors.append(f"missing local page: {p['slug']}"); continue
        local_pages.append(page); text=page.read_text(encoding="utf-8"); low=text.lower(); parser=MetaParser(); parser.feed(text); h1=" ".join(parser.h1).strip(); expected=f"{SITE_ORIGIN}/khu-vuc/{p['slug']}/"
        if parser.canonical!=expected: errors.append(f"{p['slug']}: canonical mismatch {parser.canonical}")
        if not h1 or p["name"] not in h1: errors.append(f"{p['slug']}: H1 missing province name")
        if p["name"] not in parser.title and not (p["name"]=="Thành phố Hồ Chí Minh" and "TP.HCM" in parser.title): errors.append(f"{p['slug']}: title missing province")
        if p["name"] not in parser.desc: errors.append(f"{p['slug']}: description missing province")
        if 'data-local-page="'+p["slug"]+'"' not in text: errors.append(f"{p['slug']}: data-local-page marker missing")
        if '"@type": "FAQPage"' not in text: errors.append(f"{p['slug']}: FAQPage schema missing")
        if data["admin_source"] not in text or data["code_source"] not in text: errors.append(f"{p['slug']}: official admin evidence links missing")
        if "HOLD_LOCAL_EVIDENCE" in text: errors.append(f"{p['slug']}: stale HOLD_LOCAL_EVIDENCE leaked")
        wc=word_count(text)
        if wc<700: errors.append(f"{p['slug']}: page too thin ({wc} words)")
        for phrase in FORBIDDEN_CLAIMS:
            if phrase in low: errors.append(f"{p['slug']}: forbidden unsupported local claim: {phrase}")
        for legacy in p["merged_from"]:
            if legacy!=p["name"] and legacy not in text: errors.append(f"{p['slug']}: legacy locality not explained: {legacy}")
        if f'/fpt/khu-vuc/{p["slug"]}/' not in index_text: errors.append(f"khu-vuc index missing link: {p['slug']}")
        titles.add(parser.title); descs.add(parser.desc); h1s.add(h1)

    if len(local_pages)!=34: errors.append(f"expected 34 local detail pages, got {len(local_pages)}")
    if len(titles)!=34: errors.append(f"local titles not unique: {len(titles)}/34")
    if len(descs)!=34: errors.append(f"local descriptions not unique: {len(descs)}/34")
    if len(h1s)!=34: errors.append(f"local H1s not unique: {len(h1s)}/34")
    if index_text.count('class="link-tile" href="/fpt/khu-vuc/')!=34: errors.append("khu-vuc index does not contain exactly 34 province cards")

    sitemap=(site/"sitemap.xml").read_text(encoding="utf-8")
    for p in provinces:
        loc=f"{SITE_ORIGIN}/khu-vuc/{p['slug']}/"
        if loc not in sitemap: errors.append(f"sitemap missing {p['slug']}")
    for bad in BAD_SLUGS:
        if bad in sitemap or bad in index_text: errors.append(f"legacy malformed slug still present: {bad}")

    if errors:
        print("LOCAL SEO QA FAIL"); [print("-",item) for item in errors[:100]]; raise SystemExit(1)
    print(f"LOCAL SEO QA PASS: pages=34, current_units=34, predecessor_names=63, search_aliases={sum(len(p['aliases']) for p in provinces)}, keyword_rows={len(rows)}, sitemap_local=34")


if __name__=="__main__": main()
