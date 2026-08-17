# FULL FPT SEO WEBSITE — QA REPORT

Date: 2026-08-17
Status: **PASS — integrated local pages + full keyword map validated**

## Coverage
- HTML pages in production-shaped artifact: 107
- Indexable pages / sitemap URLs: 106 / 106
- Legacy noindex handoff: 1 (`/support/`), excluded from sitemap
- Current province/city landing pages: 34
- Local keyword rows: 3,800
- Local keyword patterns: 50
- Current/legacy/common local search aliases: 76
- Provincial-unit names immediately before the June-2025 consolidation covered by the routing map: 63
- Existing non-local keyword/query mapping baseline: 1,805 rows
- Existing AEO question baseline: 277
- SEO-specific unique WebP images: 118
- Internal links checked in the integrated production-shaped artifact: 2,912

## Integrated hard gates
- Generated local pages: 34/34
- Unique local title/H1/canonical: PASS
- Local minimum content-depth gate: PASS
- Lead form on local pages: PASS
- Shared contact dock/UI motion/page transition on local pages: PASS
- Unsupported numeric province-wide price/speed claims: 0
- Local keyword rows: 3,800/3,800
- Keyword patterns: 50/50
- Search aliases: 76/76
- Current canonical local URLs: 34/34
- Pre-consolidation provincial names covered: 63/63
- Malformed historical slugs: 0
- Sitemap indexable URLs: 106
- Noindex HTML excluded from sitemap: 1
- Broken internal links: 0 in functional QA
- Missing local assets: 0
- UI legacy runtime layers: 0

## Local evidence policy
The 34 province/city pages provide administrative/address context, selection guidance, FAQ/schema, internal links and a working lead form. They do not infer that an entire province has identical FPT infrastructure, price, promotion, equipment allocation or installation time.

Former province names and common aliases are used for keyword routing only. They map to the relevant current province/city landing page instead of creating separate name-swap pages.

Administrative context is grounded in current Government publications. Address-specific FPT infrastructure, price, promotion, equipment and installation conditions remain subject to verification before being stated as current facts.

## Latest integrated QA evidence
GitHub Actions run `32042041579` reported:
- `LOCAL KEYWORDS GENERATED: 3800 rows`
- `Local pages generated: 34 + index`
- `QA PASS: 107 HTML pages, 118 SEO images, 0 forbidden internal phrases, 0 missing local assets`
- `Sitemap synced: 106 indexable HTML URLs; noindex excluded=1`
- `LOCAL QA PASS: 34/34 pages; unique title/H1/canonical; form + contact dock + UI motion + transition present; no unsupported numeric price/speed claims`
- `LOCAL KEYWORD QA PASS: current_units=34, predecessor_names=63, aliases=76, patterns=50, keyword_rows=3800, canonical_urls=34`
- `FUNCTIONAL QA PASS: pages=107, internal_links=2912, legacy_redirects=1, contact_actions=3, lead_form=ready, modem_transition=ready`
- `UI RESET QA PASS: pages=107, legacy_runtime_layers=0, mobile_content_visible=default, nav=isolated, dock=contained, motion=progressive`
- `SITEMAP URL COUNT: 106`

## Time-sensitive commercial data
Prices, promotions, equipment, local infrastructure and installation conditions must be re-verified before presenting them as current facts for a specific address.
