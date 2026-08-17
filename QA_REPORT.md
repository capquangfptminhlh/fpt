# FULL FPT SEO WEBSITE — QA REPORT

Date: 2026-08-17
Status: **PASS — full local corpus + keyword map validated on production-shaped artifact**

## Coverage
- HTML pages: 141
- Indexable pages / sitemap URLs: 140 / 140
- Legacy noindex handoff: 1 (`/support/`), excluded from sitemap
- Current province/city landing pages: 34
- Province/city news hubs: 34
- Service catalogs: 34
- Local keyword rows: 3,800
- Local keyword patterns: 50
- Current/legacy/common local search aliases: 76
- Provincial-unit names immediately before the June-2025 consolidation covered by the routing map: 63
- Existing non-local keyword/query mapping baseline: 1,805 rows
- Existing AEO question baseline: 277
- SEO-specific unique WebP images: 118
- Internal links checked: 4,285

## Local page gates
- Generated province landings: 34/34
- Unique local title/H1/canonical: PASS
- Local minimum content-depth gate: PASS
- Lead form on local landings: PASS
- Shared contact dock/UI motion/page transition: PASS
- Unsupported numeric province-wide price/speed claims: 0

## Service/news silo gates
- Service catalogs: 34/34
- Local news hubs: 34/34
- Internet links per province: 8
- FPT Play/combo links per province: 5
- Camera links per province: 3
- Unique news title/H1/canonical: PASS
- News source/disclosure markers after production sanitization: PASS
- Unsupported numeric local price/speed claims in news hubs: 0
- Pages carrying Khu vực navigation: 140

## Keyword gates
- Local keyword rows: 3,800/3,800
- Keyword patterns: 50/50
- Search aliases: 76/76
- Current canonical local URLs: 34/34
- Pre-consolidation provincial names covered: 63/63
- Malformed historical local slugs: 0
- Every alias maps to the relevant current route rather than a duplicate old-name page.

## Site-wide gates
- HTML/assets sanitizer: PASS — 141 HTML, 118 SEO images, 0 forbidden internal phrases, 0 missing local assets
- Functional QA: PASS — 4,285 internal links, 1 legacy redirect, contact actions=3, lead form ready, modem transition ready
- UI reset QA: PASS — 141/141 ordered pages, legacy runtime layers=0, mobile content visible, nav isolated, dock contained, motion progressive
- Sitemap: 140 indexable HTML URLs; noindex excluded=1

## Evidence policy
Administrative context is grounded in current Government publications for the 34 provincial-level units. Province pages and local news hubs do not infer that an entire province has identical FPT infrastructure, price, promotion, equipment allocation, speed or installation time.

Former province names and common aliases are retained for search coverage but route to the relevant current province/city page. Local news beyond the evidence-safe hub is only appropriate when there is sufficiently strong locality/time-specific sourcing.

## Latest full QA evidence
GitHub Actions run `32042314191` reported:
- `LOCAL KEYWORDS GENERATED: 3800 rows`
- `Local pages generated: 34 + index`
- `Local silos enriched: 34 catalogs + 34 news hubs`
- `QA PASS: 141 HTML pages, 118 SEO images, 0 forbidden internal phrases, 0 missing local assets`
- `Sitemap synced: 140 indexable HTML URLs; noindex excluded=1`
- `LOCAL QA PASS: 34/34 pages`
- `LOCAL SILO QA PASS: 34/34 service catalogs, 34/34 news hubs, 8 internet + 5 FPT Play/combo + 3 camera links per province`
- `LOCAL KEYWORD QA PASS: current_units=34, predecessor_names=63, aliases=76, patterns=50, keyword_rows=3800, canonical_urls=34`
- `FUNCTIONAL QA PASS: pages=141, internal_links=4285, legacy_redirects=1, contact_actions=3, lead_form=ready, modem_transition=ready`
- `UI RESET QA PASS: pages=141, legacy_runtime_layers=0`
- `FINAL HTML COUNT: 141`
- `FINAL SITEMAP URL COUNT: 140`

## Time-sensitive commercial data
Prices, promotions, equipment, local infrastructure, incidents, maintenance schedules and installation conditions must be re-verified before presenting them as current facts for a specific locality/address.
