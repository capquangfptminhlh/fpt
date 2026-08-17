# FPT Full SEO Website v2

Static FPT advisory website with SEO/AEO/GEO architecture, responsive UI, local-search coverage and evidence-based publishing gates.

## Build summary
- 107 HTML pages total: 106 indexable + 1 legacy noindex handoff.
- 106 URLs in production sitemap.
- 34 indexable province/city pages under `/khu-vuc/<slug>/` using the current provincial-level administrative structure.
- 3,800 generated local keyword rows from 50 query patterns × 76 current/legacy/search aliases.
- Local mapping covers all 63 provincial-unit names immediately before the June-2025 consolidation and routes them to 34 current canonical province/city pages instead of creating duplicate old-name pages.
- Existing non-local SEO architecture remains in place, including the prior 1,805 mapped keyword/query rows and 277 AEO questions. The local 3,800-row map is tracked separately rather than claiming an unverified deduplicated grand total.
- 118 unique SEO WebP assets (all >=1200×675).
- 3,395 internal links in the production-shaped QA artifact.
- Responsive desktop/mobile UI, lead form, contact actions, modem page transition and lightweight progressive motion.
- `robots.txt`, `sitemap.xml`, structured data, canonical ownership and automated build gates.

## Local SEO architecture

Source of truth: `data/local-provinces.json`.

The local system materializes 34 current province/city pages and maps current names, pre-consolidation province names and common search aliases to those pages. Keyword patterns cover installation, availability checks, Internet/FTTH, WiFi 6/7, Mesh, XGS-PON, packages, pricing intent, promotions intent, combo, FPT Play, Camera, gaming, SpeedX, household/business use cases and support queries.

The local pages intentionally do **not** claim that every address in a province has FPT infrastructure, one fixed price, one promotion, one device configuration or a guaranteed installation time. Those details must be verified for the actual installation address before being presented as fact.

Generation and QA:
- `scripts/generate-local-keywords.py` → `seo/local-keyword-map.csv` (3,800 rows).
- `scripts/generate-local-pages.py` → 34 detail pages + `/khu-vuc/` index + sitemap entries.
- `scripts/qa-local.py` → checks 34 current units, 63 predecessor names, 76 search aliases, keyword coverage, unique title/description/H1, canonical URLs, minimum content depth, administrative evidence links and unsupported local claims.
- GitHub Pages production build also requires exactly 106 sitemap URLs and excludes the legacy `/support/` noindex handoff from the sitemap.

## Production safeguards
1. Keep the independent-advisory disclosure; do not imply the website is the corporate FPT website.
2. Re-verify commercial prices, promotions, equipment and installation conditions before publishing time-sensitive claims.
3. Do not convert a province-level page into an address-level infrastructure claim without evidence for that address.
4. Do not create duplicate pages for historical province names; map those queries to the current province/city page.
5. Keep form, contact and local-generation QA gates passing before deployment.

See `QA_REPORT.md` for the latest evidence snapshot.
