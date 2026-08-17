from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

STATUS = "READY_LOCAL_CONTEXT"
OBSERVED_AT = "2026-08-17"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="seo/local-keyword-map.csv")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "data" / "local-provinces.json").read_text(encoding="utf-8"))
    with (root / "seo" / "local-keyword-patterns.csv").open(encoding="utf-8-sig", newline="") as fh:
        patterns = list(csv.DictReader(fh))
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["location", "keyword", "proposed_url", "current_status", "reason", "admin_source", "observed_at"])
        for p in data["provinces"]:
            target = f"/khu-vuc/{p['slug']}/"
            seen = set()
            for alias in p["aliases"]:
                for item in patterns:
                    keyword = item["pattern"].format(loc=alias.lower())
                    if keyword in seen:
                        continue
                    seen.add(keyword)
                    reason = (
                        f"Canonical local page for {p['name']}; intent={item['intent']}; cluster={item['cluster']}; "
                        "address-specific availability/pricing must be verified before claim"
                    )
                    writer.writerow([alias, keyword, target, STATUS, reason, data["admin_source"], OBSERVED_AT])
                    count += 1
    print(f"LOCAL KEYWORDS GENERATED: {count} rows -> {output.relative_to(root)}")
    if count != 3800:
        raise SystemExit(f"Expected exactly 3800 local keyword rows, got {count}")


if __name__ == "__main__":
    main()
