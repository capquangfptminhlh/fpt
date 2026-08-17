# Local SEO Production Manifest — 34 tỉnh/thành + full keyword map

Observed: 2026-08-17

## Production model
- `/khu-vuc/` is the local SEO hub.
- `scripts/generate-local-pages.py` builds `_site/khu-vuc/<slug>/index.html` for all 34 current provincial-level units.
- Each local page has a unique title, H1, administrative/address context, FAQ, Service + AdministrativeArea schema, BreadcrumbList, internal links and an embedded lead form.
- Shared production runtime is injected after generation: `ui-reset.css`, `ui-motion.css/js`, page transition with modem/WiFi loader and contact dock.
- `scripts/sync-sitemap.py` rebuilds the sitemap from indexable HTML only; noindex HTML is excluded.

## Full local keyword model
- Source: `data/local-provinces.json`.
- Pattern library: `seo/local-keyword-patterns.csv`.
- Generator: `scripts/generate-local-keywords.py`.
- Materialized map: `seo/local-keyword-map.csv`.
- Current canonical province/city routes: **34**.
- Provincial-unit names immediately before the June-2025 consolidation covered by the routing map: **63**.
- Current/legacy/common search aliases: **76**.
- Query patterns: **50**.
- Generated local keyword rows: **3,800**.

The 50 patterns cover installation, infrastructure/address checks, Internet/FTTH, WiFi, WiFi 6, WiFi 7, Mesh, XGS-PON, packages, price intent, promotion intent, combo, FPT Play, Camera, gaming, SpeedX, household/business use cases and support queries.

Former province names and common aliases map to the relevant current route. They do not create separate duplicate landing pages.

## Evidence policy
Administrative context is grounded in the Government publication covering the 34 provincial-level administrative units after the 2025 reorganization:

https://xaydungchinhsach.chinhphu.vn/chi-tiet-34-don-vi-hanh-chinh-cap-tinh-tu-12-6-2025-119250612141845533.htm

Commercial information remains address/time dependent. The local pages must not invent or generalize province-wide infrastructure coverage, price, installation fee, device allocation, promotion or guaranteed installation time. Those facts remain subject to address-level verification.

The production pages also point users to FPT Telecom's official site for current service information:

https://fpt.vn/vi/

## Canonical local routes
1. Hà Nội — `/khu-vuc/ha-noi/`
2. Cao Bằng — `/khu-vuc/cao-bang/`
3. Tuyên Quang — `/khu-vuc/tuyen-quang/`
4. Điện Biên — `/khu-vuc/dien-bien/`
5. Lai Châu — `/khu-vuc/lai-chau/`
6. Sơn La — `/khu-vuc/son-la/`
7. Lào Cai — `/khu-vuc/lao-cai/`
8. Thái Nguyên — `/khu-vuc/thai-nguyen/`
9. Lạng Sơn — `/khu-vuc/lang-son/`
10. Quảng Ninh — `/khu-vuc/quang-ninh/`
11. Bắc Ninh — `/khu-vuc/bac-ninh/`
12. Phú Thọ — `/khu-vuc/phu-tho/`
13. Hải Phòng — `/khu-vuc/hai-phong/`
14. Hưng Yên — `/khu-vuc/hung-yen/`
15. Ninh Bình — `/khu-vuc/ninh-binh/`
16. Thanh Hóa — `/khu-vuc/thanh-hoa/`
17. Nghệ An — `/khu-vuc/nghe-an/`
18. Hà Tĩnh — `/khu-vuc/ha-tinh/`
19. Quảng Trị — `/khu-vuc/quang-tri/`
20. Huế — `/khu-vuc/hue/`
21. Đà Nẵng — `/khu-vuc/da-nang/`
22. Quảng Ngãi — `/khu-vuc/quang-ngai/`
23. Gia Lai — `/khu-vuc/gia-lai/`
24. Khánh Hòa — `/khu-vuc/khanh-hoa/`
25. Đắk Lắk — `/khu-vuc/dak-lak/`
26. Lâm Đồng — `/khu-vuc/lam-dong/`
27. Đồng Nai — `/khu-vuc/dong-nai/`
28. Thành phố Hồ Chí Minh — `/khu-vuc/thanh-pho-ho-chi-minh/`
29. Tây Ninh — `/khu-vuc/tay-ninh/`
30. Cần Thơ — `/khu-vuc/can-tho/`
31. Vĩnh Long — `/khu-vuc/vinh-long/`
32. Đồng Tháp — `/khu-vuc/dong-thap/`
33. Cà Mau — `/khu-vuc/ca-mau/`
34. An Giang — `/khu-vuc/an-giang/`

## Required CI gates
`pages.yml` must pass these before deployment:
1. Generate exactly 3,800 local keyword rows.
2. Generate all 34 local pages.
3. Run the production sanitizer/path rewrite and inject shared UI/contact/transition runtime.
4. Rebuild sitemap from indexable HTML only.
5. `qa-local-pages.py` — exactly 34 routes; unique title/H1/canonical; minimum content depth; lead form/runtime/evidence disclosure present; no unsupported numeric local price/speed claims.
6. `qa-local-keywords.py` — 34 current routes, 63 predecessor names, 76 aliases, 50 patterns and 3,800 keyword rows; all aliases route to current URLs.
7. `qa-functional.py` and `qa-ui-reset.py`.
8. Python compile checks and production JavaScript syntax checks.
9. Sitemap must contain exactly 106 indexable URLs; legacy `/support/` noindex handoff must be excluded.

A local page is not considered production PASS until the GitHub Pages deployment itself succeeds after all gates above.
