# Local province service/news rollout

Production build target:
- 34 province/city landing pages under `/khu-vuc/<slug>/`.
- 34 province/city news hubs under `/khu-vuc/<slug>/tin-tuc/`.
- Visible `Khu vực` navigation on every page using the shared `nav-links` navigation.
- Per-province service catalog linking to all existing website owners:
  - 8 Internet pages: Giga, Sky, Meta, F-Game, SpeedX2, SpeedX2 Pro, SpeedX10, SpeedX10 Pro.
  - 5 FPT Play/combo destinations: Combo Giga, Combo Sky, Combo Meta, Combo F-Game, FPT Play.
  - 3 Camera destinations: Camera FPT, Camera Play 3, Camera Play 4.

Evidence policy:
- No local numeric price/speed claims without address/time evidence.
- No invented local promotions, incidents, maintenance schedules, infrastructure coverage or product names.
- Local news is a verified-source hub; articles are only added when local evidence passes editorial/QA gates.

QA evidence from Run #52 attempt 2 and Run #53 attempt 2 before GitHub Pages returned HTTP 503:
- 141 HTML pages.
- 141 sitemap URLs.
- Local page QA PASS 34/34.
- Local silo QA PASS 34/34 service catalogs + 34/34 news hubs.
- 8 Internet + 5 FPT Play/combo + 3 Camera links per province.
- `Khu vực` navigation checked on 140 pages.
- Functional QA PASS with 4,412 internal links.
- UI reset QA PASS on 141/141 pages.
- Artifact upload PASS; Pages deployment creation alone returned transient HTTP 503.

This file is documentation only and records the production checkpoint while triggering a fresh GitHub Pages run after the transient Pages deployment failure.
