# Local province service/news rollout

Production build target:
- 34 province/city landing pages under `/khu-vuc/<slug>/`.
- 34 province/city news hubs under `/khu-vuc/<slug>/tin-tuc/`.
- Visible `Khu vực` navigation across the shared navigation pages.
- Per-province service catalog linking to all existing website owners:
  - 8 Internet pages: Giga, Sky, Meta, F-Game, SpeedX2, SpeedX2 Pro, SpeedX10, SpeedX10 Pro.
  - 5 FPT Play/combo destinations: Combo Giga, Combo Sky, Combo Meta, Combo F-Game, FPT Play.
  - 3 Camera destinations: Camera FPT, Camera Play 3, Camera Play 4.
- Full local keyword routing: 3,800 rows from 50 patterns × 76 current/legacy/search aliases, covering 63 provincial-unit names immediately before the June-2025 consolidation and mapping them to 34 current routes.

Evidence policy:
- No local numeric price/speed claims without address/time evidence.
- No invented local promotions, incidents, maintenance schedules, infrastructure coverage or product names.
- Local news is a verified-source hub; articles are only added when local evidence passes editorial/QA gates.

Latest validated production-shaped target:
- 141 HTML pages total.
- 140 indexable sitemap URLs; legacy `/support/` remains noindex and is excluded.
- Local page QA PASS 34/34.
- Local silo QA PASS 34/34 service catalogs + 34/34 news hubs.
- Local keyword QA PASS: 34 current routes, 63 predecessor names, 76 aliases, 50 patterns, 3,800 rows.
- 8 Internet + 5 FPT Play/combo + 3 Camera links per province.
- `Khu vực` navigation checked on 140 pages and normalized on 127 pages in final-merge QA.
- Functional QA PASS with 4,412 internal links.
- UI reset QA PASS on 141/141 pages.

The earlier GitHub Pages HTTP 503 was a transient deployment-layer failure; content/build gates are evaluated separately and production is only considered complete after a later Pages deployment succeeds.
