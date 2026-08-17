# Local province service/news rollout

Production build target:
- 34 province/city landing pages under `/khu-vuc/<slug>/`.
- 34 province/city news hubs under `/khu-vuc/<slug>/tin-tuc/`.
- Visible `Khu vực` navigation across the shared navigation pages.
- Per-province service catalog: 8 Internet + 5 FPT Play/combo + 3 Camera destinations.
- Full local keyword routing: 3,800 rows from 50 patterns × 76 current/legacy/search aliases, covering 63 provincial-unit names immediately before the June-2025 consolidation and mapping them to 34 current routes.

Evidence policy:
- No local numeric price/speed claims without address/time evidence.
- No invented local promotions, incidents, maintenance schedules, infrastructure coverage or product names.
- Local news is a verified-source hub; articles are only added when local evidence passes editorial/QA gates.

Deployment history and corrected checkpoint:
- Runs #52 and #53 reached artifact upload but GitHub Pages deployment creation returned transient HTTP 503; that was a deployment-layer failure, not a content QA pass/fail signal.
- Final merged-head QA run `32043141500` completed successfully before production merge.
- Final validated artifact: 141 HTML pages total, 140 indexable sitemap URLs, legacy `/support/` noindex excluded.
- Local page QA: 34/34 PASS.
- Local silo QA: 34/34 service catalogs + 34/34 news hubs PASS.
- Local keyword QA: 34 current routes, 63 predecessor names, 76 aliases, 50 patterns, 3,800 rows PASS.
- `Khu vực` navigation checked on 140 pages and normalized on 127 pages.
- Functional QA: 4,412 internal links PASS.
- UI reset QA: 141/141 pages PASS.

Production is only considered complete after the subsequent GitHub Pages deployment itself reports success.
