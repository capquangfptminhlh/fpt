from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

EXPECTED_ROWS = 3800
EXPECTED_PATTERNS = 50
EXPECTED_CURRENT = 34
EXPECTED_PREDECESSOR_NAMES = 63
EXPECTED_ALIASES = 76
BAD_SLUGS = {"a-nang", "ak-lak", "ien-bien", "ong-nai", "ong-thap"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    site = Path(args.site)
    config = json.loads((root / "data" / "local-provinces.json").read_text(encoding="utf-8"))
    provinces = config["provinces"]

    errors: list[str] = []
    if len(provinces) != EXPECTED_CURRENT:
        errors.append(f"current province config: expected {EXPECTED_CURRENT}, got {len(provinces)}")

    current_slugs = {p["slug"] for p in provinces}
    if len(current_slugs) != EXPECTED_CURRENT:
        errors.append(f"current slugs not unique: {len(current_slugs)}")

    built_slugs = {p.parent.name for p in (site / "khu-vuc").glob("*/index.html")}
    if current_slugs != built_slugs:
        errors.append(
            "keyword source and built local routes differ: "
            f"missing={sorted(current_slugs - built_slugs)} extra={sorted(built_slugs - current_slugs)}"
        )

    predecessor_names = {name for p in provinces for name in p["merged_from"]}
    if len(predecessor_names) != EXPECTED_PREDECESSOR_NAMES:
        errors.append(
            f"pre-consolidation provincial names: expected {EXPECTED_PREDECESSOR_NAMES}, got {len(predecessor_names)}"
        )

    alias_count = sum(len(p["aliases"]) for p in provinces)
    if alias_count != EXPECTED_ALIASES:
        errors.append(f"search aliases: expected {EXPECTED_ALIASES}, got {alias_count}")

    patterns_path = root / "seo" / "local-keyword-patterns.csv"
    with patterns_path.open(encoding="utf-8-sig", newline="") as fh:
        patterns = list(csv.DictReader(fh))
    if len(patterns) != EXPECTED_PATTERNS:
        errors.append(f"keyword patterns: expected {EXPECTED_PATTERNS}, got {len(patterns)}")
    if len({row["pattern"] for row in patterns}) != len(patterns):
        errors.append("duplicate keyword pattern")

    map_path = root / "seo" / "local-keyword-map.csv"
    with map_path.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) != EXPECTED_ROWS:
        errors.append(f"keyword rows: expected {EXPECTED_ROWS}, got {len(rows)}")

    pair_counts = Counter((r["keyword"], r["proposed_url"]) for r in rows)
    duplicates = [pair for pair, count in pair_counts.items() if count > 1]
    if duplicates:
        errors.append(f"duplicate keyword/url pairs: {len(duplicates)}")

    rows_by_location: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    rows_by_url: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        rows_by_location[(row["location"], row["proposed_url"])].append(row)
        rows_by_url[row["proposed_url"]].append(row)
        if row["current_status"] != "READY_LOCAL_CONTEXT":
            errors.append(f"unexpected keyword status: {row['current_status']}")
            break
        if "address-specific availability/pricing must be verified before claim" not in row["reason"]:
            errors.append(f"missing evidence qualifier for keyword: {row['keyword']}")
            break

    expected_urls = {f"/khu-vuc/{p['slug']}/" for p in provinces}
    actual_urls = set(rows_by_url)
    if expected_urls != actual_urls:
        errors.append(
            f"keyword canonical URL set mismatch: missing={sorted(expected_urls-actual_urls)} extra={sorted(actual_urls-expected_urls)}"
        )

    for p in provinces:
        url = f"/khu-vuc/{p['slug']}/"
        page = site / "khu-vuc" / p["slug"] / "index.html"
        page_text = page.read_text(encoding="utf-8") if page.exists() else ""
        for alias in p["aliases"]:
            alias_rows = rows_by_location[(alias, url)]
            if len(alias_rows) != EXPECTED_PATTERNS:
                errors.append(f"{p['slug']}: alias {alias!r} has {len(alias_rows)} rows, expected {EXPECTED_PATTERNS}")
        expected_page_rows = EXPECTED_PATTERNS * len(p["aliases"])
        if len(rows_by_url[url]) != expected_page_rows:
            errors.append(
                f"{p['slug']}: URL has {len(rows_by_url[url])} keyword rows, expected {expected_page_rows}"
            )
        for old_name in p["merged_from"]:
            if old_name != p["name"] and old_name not in page_text:
                errors.append(f"{p['slug']}: generated page does not explain predecessor locality {old_name}")

    leaked = sorted(slug for slug in BAD_SLUGS if any(f"/khu-vuc/{slug}/" in r["proposed_url"] for r in rows))
    if leaked:
        errors.append(f"malformed legacy slugs in keyword map: {leaked}")

    if errors:
        print("LOCAL KEYWORD QA FAIL")
        for item in errors[:100]:
            print(f"- {item}")
        return 1

    print(
        "LOCAL KEYWORD QA PASS: "
        f"current_units={EXPECTED_CURRENT}, predecessor_names={EXPECTED_PREDECESSOR_NAMES}, "
        f"aliases={EXPECTED_ALIASES}, patterns={EXPECTED_PATTERNS}, keyword_rows={EXPECTED_ROWS}, canonical_urls=34"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
