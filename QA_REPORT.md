# FULL FPT SEO WEBSITE — QA REPORT

Date: 2026-08-17
Status: **PASS — local expansion validated on production-shaped artifact**

## Coverage
- HTML pages: 107
- Indexable pages / sitemap URLs: 106 / 106
- Legacy noindex handoff: 1 (`/support/`), excluded from sitemap
- Existing non-local keyword/query mappings: 1,805 baseline rows
- AEO questions mapped: 277 baseline questions
- Current province/city pages: 34
- Local keyword rows: 3,800
- Local keyword patterns: 50
- Local search aliases: 76
- Provincial-unit names immediately before June-2025 consolidation covered by the map: 63
- SEO-specific unique WebP images: 118
- Production-shaped internal links checked: 3,395

## Hard gates
- Broken internal links: 0 in production-shaped QA
- Missing local CSS/JS/images: 0
- Missing generated local province page: 0
- Duplicate local title: 0
- Duplicate local description: 0
- Duplicate local H1: 0
- Local canonical mismatches: 0
- Missing local FAQPage schema: 0
- Missing administrative evidence links: 0
- Unsupported blanket local claim phrases: 0
- Malformed legacy local slugs (`a-nang`, `ak-lak`, `ien-bien`, `ong-nai`, `ong-thap`): 0
- Local pages below the minimum content-depth gate: 0
- Legacy noindex page present in sitemap: 0
- UI reset legacy runtime layers: 0

## Local SEO evidence
The local source of truth is `data/local-provinces.json`. It tracks the 34 current provincial-level units, current administrative codes, predecessor names used for search routing, common aliases and official administrative references.

The build creates one current province/city page per canonical local URL. Searches using former province names are mapped to the relevant current page instead of generating separate name-swap pages. This keeps the 34-page local architecture compact while retaining keyword coverage for older locality wording.

Local service facts remain evidence-bounded: a province page may explain how to check an address, choose Internet/WiFi/Camera/Combo by need, and interpret the current administrative context, but it does not assert province-wide FPT infrastructure, a universal local price, a universal promotion, fixed equipment or guaranteed installation time without address-specific evidence.

## Latest production-shaped QA evidence
Materialization/QA run `32041445018` reported:
- `LOCAL KEYWORDS GENERATED: 3800 rows`
- `QA PASS: 107 HTML pages, 118 SEO images, 0 forbidden internal phrases, 0 missing local assets`
- `FUNCTIONAL QA PASS: pages=107, internal_links=3395, legacy_redirects=1`
- `UI RESET QA PASS: pages=107, legacy_runtime_layers=0`
- `LOCAL SEO QA PASS: pages=34, current_units=34, predecessor_names=63, search_aliases=76, keyword_rows=3800, sitemap_local=34`
- `SITEMAP URL COUNT: 106`
- Second materialization pass: `No materialized changes to commit.`

## Time-sensitive commercial data
Prices, promotions, equipment, local infrastructure and installation conditions must still be re-verified before presenting them as current facts for a specific address.
