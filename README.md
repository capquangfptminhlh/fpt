# FPT Full SEO Website v2

Static FPT advisory website with SEO/AEO/GEO architecture, responsive UI, local-search coverage and evidence-based publishing gates.

## Build summary
- 107 HTML pages in the production-shaped build: 106 indexable + 1 legacy noindex handoff.
- 106 indexable URLs in the sitemap.
- 34 current province/city landing pages under `/khu-vuc/<slug>/`.
- 3,800 local keyword rows generated from 50 query patterns × 76 current/legacy/search aliases.
- Local search routing covers all 63 provincial-unit names immediately before the June-2025 consolidation and maps them into the 34 current province/city routes rather than creating duplicate old-name pages.
- Existing non-local SEO baseline remains tracked separately: 1,805 mapped keyword/query rows and 277 AEO questions. The local 3,800-row map is intentionally reported separately instead of claiming an unverified deduplicated grand total.
- 118 unique SEO WebP assets (all >=1200×675).
- Responsive desktop/mobile UI, lead forms on local pages, contact actions, modem page transition and lightweight progressive motion.
- `robots.txt`, indexable-only `sitemap.xml`, structured data, canonical ownership and automated build gates.

## Local SEO architecture

The local landing-page generator is `scripts/generate-local-pages.py`. It builds 34 evidence-safe province/city pages with unique title/H1, administrative/address context, FAQ, Service + AdministrativeArea schema, BreadcrumbList, internal links and a working lead form.

The full keyword source is `data/local-provinces.json` + `seo/local-keyword-patterns.csv`. `scripts/generate-local-keywords.py` materializes `seo/local-keyword-map.csv` with exactly 3,800 rows.

Keyword clusters cover installation, address/infrastructure checks, Internet/FTTH, WiFi 6/7, Mesh, XGS-PON, packages, pricing intent, promotion intent, combo, FPT Play, Camera, gaming, SpeedX, household/business use cases and support queries.

Former province names and common aliases are retained for search coverage but point to the current administrative route. They do not receive separate name-swap landing pages.

## Evidence rules
- Administrative context is grounded in current Government publications for the 34 provincial-level units.
- Province pages do **not** claim that every address has FPT infrastructure.
- Province pages do **not** invent a universal local price, promotion, device allocation, installation fee or installation time.
- Commercial facts remain address/time dependent and must be re-verified before being presented as current facts for a specific installation address.
- The website keeps an independent-advisory disclosure and does not present itself as the corporate FPT website.

## Production gates
Before GitHub Pages can deploy, CI must pass:
1. Generate the 3,800-row local keyword map.
2. Generate all 34 local landing pages.
3. Apply the production sanitizer and shared UI runtime.
4. Build the sitemap from indexable HTML only.
5. `qa-local-pages.py` for page depth, unique title/H1/canonical, forms, schema/runtime and unsupported price/speed claims.
6. `qa-local-keywords.py` for 34 current routes, 63 predecessor names, 76 aliases, 50 patterns and exactly 3,800 keyword rows.
7. Functional/UI-reset QA and production JavaScript syntax checks.
8. Sitemap must contain exactly 106 indexable URLs; the legacy `/support/` noindex handoff must stay out of the sitemap.

See `QA_REPORT.md` and `seo/local-pages-manifest.md` for evidence and route details.
