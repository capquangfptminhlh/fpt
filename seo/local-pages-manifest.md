# Local SEO Production Manifest — 34 tỉnh/thành + service/news silos + full keyword map

Observed: 2026-08-17

## Production model
- `/khu-vuc/` is the local SEO hub.
- `scripts/generate-local-pages.py` builds 34 current province/city landing pages.
- `scripts/enrich-local-silos.py` adds 34 service catalogs and creates 34 province/city news hubs at `/khu-vuc/<slug>/tin-tuc/`.
- `scripts/fix-local-nav.py` normalizes visible `Khu vực` navigation across the final artifact.
- Each landing has unique title/H1/canonical, administrative/address context, FAQ, Service + AdministrativeArea schema, BreadcrumbList, internal links and lead form.
- Each service catalog links 8 Internet entries, 5 FPT Play/combo entries and 3 Camera entries already represented on the website.
- Each news hub has unique title/H1/canonical, evidence/source guidance and links back to its province service catalog.
- `scripts/sync-sitemap.py` rebuilds the sitemap from indexable HTML only.

## Full keyword model
- Province/alias source: `data/local-provinces.json`.
- Pattern library: `seo/local-keyword-patterns.csv`.
- Generator: `scripts/generate-local-keywords.py`.
- Materialized map: `seo/local-keyword-map.csv`.
- Current canonical province/city routes: **34**.
- Provincial-unit names immediately before the June-2025 consolidation covered by search routing: **63**.
- Current/legacy/common search aliases: **76**.
- Query patterns: **50**.
- Generated local keyword rows: **3,800**.

Patterns cover installation, address/infrastructure checks, Internet/FTTH, WiFi, WiFi 6/7, Mesh, XGS-PON, packages, price intent, promotion intent, combo, FPT Play, Camera, gaming, SpeedX, household/business use cases and support queries.

Former province names and common aliases map to the relevant current province/city route. They do not create separate duplicate landing pages.

## Evidence policy
Administrative context is grounded in current Government publications for the 34 provincial-level units after the 2025 reorganization. Commercial information remains address/time dependent. Province pages and news hubs must not invent or generalize province-wide infrastructure coverage, price, installation fee, device allocation, speed, promotion, outage or maintenance schedule.

Government administrative source:
https://xaydungchinhsach.chinhphu.vn/chi-tiet-34-don-vi-hanh-chinh-cap-tinh-tu-12-6-2025-119250612141845533.htm

FPT Telecom public service reference:
https://fpt.vn/vi/

## Canonical province routes
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

Each route also owns its `/tin-tuc/` hub.

## Required CI gates
Production CI must generate the 3,800-keyword map, 34 landings, 34 service catalogs and 34 news hubs; normalize Khu vực navigation; sanitize/inject the shared runtime; build sitemap from indexable HTML only; then pass local page, silo, keyword, functional, UI, Python and JavaScript checks.

Final artifact requirements: exactly **141 HTML pages**, **140 indexable sitemap URLs**, legacy `/support/` remains noindex and outside sitemap.

Final merge QA run `32042599336` passed all gates with **4,412 internal links** checked; `Khu vực` navigation was checked on **140 pages** and normalized on **127 pages**.
