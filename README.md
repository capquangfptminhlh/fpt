# FPT Full SEO Website v2

Static FPT advisory website with SEO/AEO/GEO architecture, responsive UI, local-search coverage and evidence-based publishing gates.

## Build summary
- 141 HTML pages in the final production-shaped build: 140 indexable + 1 legacy noindex handoff.
- 140 indexable URLs in the sitemap.
- 34 current province/city landing pages under `/khu-vuc/<slug>/`.
- 34 province/city news hubs under `/khu-vuc/<slug>/tin-tuc/`.
- Every province landing contains a service catalog linking 8 Internet packages, 5 FPT Play/combo entries and 3 Camera entries already present on the website.
- 3,800 local keyword rows generated from 50 query patterns × 76 current/legacy/search aliases.
- Local search routing covers all 63 provincial-unit names immediately before the June-2025 consolidation and maps them into the 34 current province/city routes rather than creating duplicate old-name pages.
- Existing non-local SEO baseline remains tracked separately: 1,805 mapped keyword/query rows and 277 AEO questions. The local 3,800-row map is intentionally reported separately instead of claiming an unverified deduplicated grand total.
- 118 unique SEO WebP assets (all >=1200×675).
- 4,285 internal links checked in final QA.
- Responsive desktop/mobile UI, lead forms on province landings, contact actions, modem page transition and lightweight progressive motion.
- `robots.txt`, indexable-only `sitemap.xml`, structured data, canonical ownership and automated build gates.

## Local SEO architecture

### Province landing pages
`scripts/generate-local-pages.py` builds 34 current province/city landing pages with unique title/H1/canonical, administrative/address context, FAQ, Service + AdministrativeArea schema, BreadcrumbList, internal links and a working lead form.

### Service and news silos
`scripts/enrich-local-silos.py` adds a service catalog to every province landing and creates 34 local news hubs. The news hubs are evidence-gated: they are not allowed to fabricate a local promotion, outage, maintenance schedule, price, speed or infrastructure claim without a source for that locality and time.

### Full local keyword map
The keyword source is `data/local-provinces.json` + `seo/local-keyword-patterns.csv`. `scripts/generate-local-keywords.py` materializes `seo/local-keyword-map.csv` with exactly 3,800 rows.

The 50 patterns cover installation, address/infrastructure checks, Internet/FTTH, WiFi 6/7, Mesh, XGS-PON, packages, pricing intent, promotion intent, combo, FPT Play, Camera, gaming, SpeedX, household/business use cases and support queries.

Former province names and common aliases are retained for search coverage but point to the current administrative route. They do not receive separate name-swap landing pages.

## Evidence rules
- Administrative context is grounded in current Government publications for the 34 provincial-level units.
- Province pages do **not** claim that every address has FPT infrastructure.
- Province pages do **not** invent a universal local price, promotion, device allocation, installation fee, speed or installation time.
- Commercial facts remain address/time dependent and must be re-verified before being presented as current facts for a specific installation address.
- Local news only moves beyond hub-level content when there is sufficiently strong local/time-specific evidence.
- The website keeps an independent-advisory disclosure and does not present itself as the corporate FPT website.

## Production gates
Before GitHub Pages can deploy, CI must pass:
1. Generate exactly 3,800 local keyword rows.
2. Generate all 34 province/city landing pages.
3. Add all 34 service catalogs and 34 local news hubs.
4. Apply the production sanitizer and shared UI runtime.
5. Build the sitemap from indexable HTML only.
6. `qa-local-pages.py` for landing-page depth, unique title/H1/canonical, forms, schema/runtime and unsupported numeric local price/speed claims.
7. `qa-local-silos.py` for 34 service catalogs, 34 news hubs, product-link counts, source/disclosure markers and global Khu vực navigation.
8. `qa-local-keywords.py` for 34 current routes, 63 predecessor names, 76 aliases, 50 patterns and exactly 3,800 keyword rows.
9. Functional/UI-reset QA, Python compile checks and production JavaScript syntax checks.
10. Final artifact must contain exactly 141 HTML pages and 140 indexable sitemap URLs; legacy `/support/` must remain noindex and outside the sitemap.

See `QA_REPORT.md` and `seo/local-pages-manifest.md` for evidence and route details.
