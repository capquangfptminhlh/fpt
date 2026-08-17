from __future__ import annotations

import argparse
import ast
import re
from html import escape
from pathlib import Path

FOCUS = {
    'ha-noi': 'Khi địa chỉ là căn hộ, nhà phố hoặc văn phòng, hãy mô tả tầng lắp đặt và vị trí dự kiến đặt modem; cùng một gói nhưng cách bố trí Wi‑Fi có thể quyết định trải nghiệm nhiều hơn việc tăng tốc độ danh nghĩa.',
    'cao-bang': 'Nếu vị trí cần lắp được mô tả bằng thôn, xóm hoặc mốc gần nhà, hãy ghi thêm xã/phường hiện hành và số điện thoại có thể liên hệ khi kỹ thuật cần xác định chính xác điểm kéo cáp.',
    'tuyen-quang': 'Địa bàn hiện hành có thể đi kèm cách gọi Hà Giang hoặc Tuyên Quang trên giấy tờ cũ; ghi cả tên hiện tại và tên quen dùng giúp hạn chế việc đối chiếu nhầm khu vực.',
    'dien-bien': 'Với địa chỉ khó mô tả bằng số nhà, nên bổ sung tổ, bản, mốc gần vị trí lắp và nhu cầu thực tế thay vì chỉ gửi tên tỉnh rồi chọn gói theo giá.',
    'lai-chau': 'Khi địa chỉ sử dụng cách gọi thôn, bản hoặc tổ dân phố, thông tin mốc gần nhà và số tầng/phòng cần phủ Wi‑Fi giúp buổi tư vấn đi thẳng vào phương án thiết bị.',
    'son-la': 'Nếu nhà có nhiều phòng hoặc nhiều tầng, hãy tách rõ nhu cầu đường truyền và nhu cầu phủ sóng; mua gói tốc độ cao nhưng đặt một điểm phát không phù hợp vẫn có thể cho trải nghiệm kém.',
    'lao-cai': 'Người dùng có địa chỉ từng ghi Yên Bái nên giữ thêm tên tỉnh cũ trong ghi chú. Mục tiêu là để việc kiểm tra địa chỉ diễn ra chính xác trước khi so sánh GIGA, SKY, META hay các combo khác.',
    'thai-nguyen': 'Nếu địa chỉ từng thuộc Bắc Kạn, hãy ghi thêm tên cũ khi gửi yêu cầu. Với nhà ở kết hợp kinh doanh, cũng nên nêu số thiết bị bán hàng, camera và máy tính cần hoạt động liên tục.',
    'lang-son': 'Đừng chọn gói chỉ theo tốc độ quảng bá. Hãy mô tả số người dùng, vị trí modem, số phòng và thiết bị quan trọng để xác định nên ưu tiên băng thông, Access Point hay giải pháp Camera.',
    'quang-ninh': 'Với nhà ở, cửa hàng hoặc cơ sở lưu trú, hãy tách nhu cầu của khách, thiết bị nội bộ và camera. Cách chia nhóm này giúp tránh mua gói cao nhưng vẫn thiếu vùng phủ hoặc thiếu upload.',
    'bac-ninh': 'Nếu địa chỉ vẫn dùng cách gọi Bắc Giang trước sắp xếp, hãy ghi thêm tên cũ. Với nhà ở kết hợp xưởng hoặc cửa hàng, cần mô tả số thiết bị và khu vực cần Wi‑Fi thay vì chỉ chọn theo giá.',
    'phu-tho': 'Địa bàn hiện hành hợp nhất từ Phú Thọ, Vĩnh Phúc và Hòa Bình; vì vậy tên xã/phường hiện tại, tỉnh cũ và mốc gần vị trí lắp là ba lớp thông tin hữu ích khi kiểm tra địa chỉ.',
    'hai-phong': 'Nếu vị trí trước đây thuộc Hải Dương, nên ghi thêm tên cũ. Với căn hộ, nhà phố hay cơ sở kinh doanh, hãy nêu rõ số tầng và nhu cầu FPT Play/Camera để tránh phải đổi phương án sau.',
    'hung-yen': 'Địa chỉ có thể vẫn được gọi theo Hưng Yên hoặc Thái Bình trước sắp xếp. Khi gửi yêu cầu, thêm tên cũ và mô tả nhu cầu giúp việc kiểm tra khu vực và chọn thiết bị rõ ràng hơn.',
    'ninh-binh': 'Vì địa bàn hiện hành liên quan Hà Nam, Nam Định và Ninh Bình trước sắp xếp, việc ghi tỉnh cũ trong ghi chú rất hữu ích; sau đó mới nên so sánh gói theo số người, số tầng và mức upload.',
    'thanh-hoa': 'Với nhà có khoảng cách lớn giữa các phòng, hãy xem vùng phủ là một bài toán riêng. Access Point hoặc Mesh phù hợp thường quan trọng không kém việc nâng từ một gói Internet sang gói cao hơn.',
    'nghe-an': 'Khi nhu cầu gồm học online, làm việc, livestream hoặc camera, hãy tách từng luồng sử dụng. Việc này giúp biết khi nào upload và độ ổn định quan trọng hơn con số download lớn.',
    'ha-tinh': 'Địa chỉ cụ thể và sơ đồ sử dụng trong nhà nên được chuẩn bị trước khi hỏi giá. Nếu có camera, TV, máy chơi game hoặc máy tính làm việc, hãy liệt kê để tư vấn thiết bị sát nhu cầu.',
    'quang-tri': 'Nếu giấy tờ hoặc cách gọi địa chỉ còn dùng Quảng Bình, hãy ghi thêm tên cũ. Với nhu cầu gia đình, hãy mô tả khu vực cần Wi‑Fi và thiết bị quan trọng trước khi chọn combo.',
    'hue': 'Nhà nhiều tầng, homestay hoặc cửa hàng có thể cần cách bố trí thiết bị khác nhau. Hãy xem modem, Access Point/Mesh và đường dây đến thiết bị cố định như một phần của lựa chọn gói.',
    'da-nang': 'Nếu địa chỉ trước đây thuộc Quảng Nam, hãy giữ tên cũ trong ghi chú. Với nhu cầu vừa ở vừa kinh doanh, nên tách mạng cho khách, thiết bị nội bộ và camera để chọn cấu hình hợp lý.',
    'quang-ngai': 'Địa bàn hiện hành có khu vực từng thuộc Kon Tum; ghi thêm tên cũ giúp xác minh. Nếu vị trí có nhiều phòng hoặc khoảng cách lớn, hãy mô tả vùng cần phủ Wi‑Fi thay vì chỉ chọn băng thông.',
    'gia-lai': 'Nếu địa chỉ trước đây thuộc Bình Định, nên ghi tên cũ trong yêu cầu. Với nhà ở, cửa hàng hay văn phòng nhỏ, số người dùng và số điểm cần phủ Wi‑Fi là dữ liệu cần có trước khi chốt gói.',
    'khanh-hoa': 'Nếu địa chỉ từng ghi Ninh Thuận, hãy bổ sung tên cũ. Nếu dùng camera hoặc livestream, hãy nêu rõ số camera và thiết bị upload để không chọn gói chỉ theo download.',
    'dak-lak': 'Nếu vị trí trước đây thuộc Phú Yên, hãy ghi tên cũ cùng địa chỉ hiện hành. Với nhà nhiều phòng, cần xác định cả tốc độ đường truyền lẫn phương án điểm phát Wi‑Fi.',
    'lam-dong': 'Địa bàn hiện hành liên quan Lâm Đồng, Bình Thuận và Đắk Nông trước sắp xếp; ghi thêm tỉnh cũ giúp đối chiếu. Với cơ sở lưu trú hoặc nhà lớn, hãy tách nhu cầu khách và thiết bị nội bộ.',
    'dong-nai': 'Nếu địa chỉ trước đây thuộc Bình Phước, nên bổ sung tên cũ. Với nhà ở kết hợp kinh doanh, số thiết bị, camera và khu vực cần phủ sóng nên được ghi ngay trong yêu cầu đầu tiên.',
    'thanh-pho-ho-chi-minh': 'Địa chỉ hiện hành có thể vẫn quen gọi theo TP.HCM, Bình Dương hoặc Bà Rịa - Vũng Tàu trước sắp xếp. Ghi cả tên cũ, phường/xã hiện tại và loại công trình giúp giảm nhầm lẫn khi kiểm tra.',
    'tay-ninh': 'Nếu địa chỉ trước đây thuộc Long An, hãy giữ tên cũ trong ghi chú. Với nhà ở hoặc cửa hàng, nên liệt kê thiết bị cố định, camera và số khu vực cần Wi‑Fi trước khi so sánh gói.',
    'can-tho': 'Nếu địa chỉ từng thuộc Hậu Giang hoặc Sóc Trăng, hãy ghi thêm tên cũ. Với nhà nhiều người dùng, cần phân biệt nhu cầu xem video, làm việc, game và camera để chọn băng thông phù hợp.',
    'vinh-long': 'Địa chỉ có thể liên quan Vĩnh Long, Bến Tre hoặc Trà Vinh trước sắp xếp. Khi gửi yêu cầu, ghi tên cũ và mô tả số tầng/phòng sẽ hữu ích hơn việc chỉ hỏi “gói nào rẻ nhất”.',
    'dong-thap': 'Nếu địa chỉ trước đây thuộc Tiền Giang, hãy ghi thêm tên cũ. Với gia đình có camera hoặc làm việc từ xa, hãy chú ý upload, vùng phủ và vị trí thiết bị cố định.',
    'ca-mau': 'Nếu địa chỉ từng thuộc Bạc Liêu, nên giữ tên cũ trong ghi chú. Nếu nhà có nhiều khu vực cần quan sát, hãy lập danh sách vị trí camera trước để so sánh mua lẻ, combo camera hay Internet + Camera.',
    'an-giang': 'Nếu địa chỉ trước đây thuộc Kiên Giang, hãy ghi thêm tên cũ. Với nhu cầu nhà ở, cửa hàng hoặc cơ sở dịch vụ, hãy mô tả số người dùng, camera và khu vực cần Wi‑Fi trước khi chốt cấu hình.',
}


def load_locations(path: Path) -> list[dict]:
    tree = ast.parse(path.read_text(encoding='utf-8'))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'LOCATIONS' for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit('LOCAL EDITORIAL BUILD FAIL: LOCATIONS not found')


def admin_copy(loc: dict) -> tuple[str, str]:
    name = loc['name']
    merged = loc.get('merged_from') or []
    if len(merged) > 1:
        old = ', '.join(merged)
        return (
            f"{name} hiện hành có liên hệ hành chính với các địa danh cấp tỉnh trước sắp xếp: {old}. Nếu hợp đồng thuê nhà, hóa đơn hoặc cách gọi địa chỉ của bạn còn dùng tên cũ, hãy ghi thêm tên đó trong phần ghi chú.",
            ''.join(f'<li>{escape(x)}</li>' for x in merged),
        )
    return (
        f"{name} giữ nguyên tên đơn vị cấp tỉnh trong đợt sắp xếp 2025. Dù vậy, khi kiểm tra dịch vụ vẫn cần ghi xã/phường hiện hành, đường/khu vực, số nhà hoặc mốc gần vị trí lắp.",
        f'<li>{escape(name)}</li>',
    )


def section(loc: dict, idx: int) -> str:
    name = loc['name']
    slug = loc['slug']
    focus = FOCUS[slug]
    admin, admin_list = admin_copy(loc)
    profile_order = [
        ('Gia đình cơ bản', 'Học tập, xem phim, mạng xã hội', 'Ưu tiên độ ổn định, Wi‑Fi 6 và vị trí modem hợp lý.'),
        ('Nhiều thiết bị', 'TV 4K, điện thoại, laptop, IoT', 'Xem băng thông và số thiết bị đồng thời; cân nhắc SKY/META hoặc nhóm cao hơn.'),
        ('Game / livestream', 'Độ trễ thấp và upload ổn định', 'So sánh F‑Game, upload, kết nối dây cho thiết bị quan trọng và vùng phủ.'),
        ('Nhà nhiều tầng', 'Cần tín hiệu ở nhiều phòng/tầng', 'Tập trung Access Point/Mesh; không dùng tốc độ danh nghĩa để thay thế bài toán vùng phủ.'),
        ('Camera / smart home', 'Nhiều luồng upload liên tục', 'Đếm số camera, vị trí trong/ngoài nhà, Cloud và độ ổn định upload.'),
        ('Cửa hàng / doanh nghiệp', 'POS, camera, họp, máy tính, khách', 'Tách thiết bị nghiệp vụ khỏi khách; xem Lux/Super Biz nếu nhu cầu vượt nhóm dân dụng.'),
    ]
    if idx % 2:
        profile_order = profile_order[2:] + profile_order[:2]
    rows = ''.join(f'<tr><td><strong>{a}</strong></td><td>{b}</td><td>{c}</td></tr>' for a,b,c in profile_order)
    scenario_cards = [
        ('Nhà 1–2 tầng', 'Bắt đầu bằng vị trí modem trung tâm. Nếu có phòng xa hoặc vật cản, kiểm tra trước khi quyết định cần Access Point/Mesh.'),
        ('Nhà nhiều tầng', 'Mỗi tầng cần được xem như một vùng phủ. Hãy hỏi rõ số Access Point/Mesh đi kèm thay vì chỉ hỏi “gói bao nhiêu Mbps”.'),
        ('Căn hộ', 'Ưu tiên vị trí modem, nhiễu Wi‑Fi và thiết bị cố định. Máy chơi game/PC làm việc nên cân nhắc kết nối dây khi có thể.'),
        ('Cửa hàng/văn phòng', 'Liệt kê POS, camera, máy tính, TV, máy in và Wi‑Fi khách để chọn nhóm gói và thiết bị đúng vai trò.'),
        ('Game/streaming', 'Quan tâm độ trễ, upload và đường dây đến thiết bị chơi game/stream. Tốc độ download cao không tự giải quyết mọi vấn đề ping.'),
        ('Camera', 'Đếm camera, độ phân giải, vị trí trong/ngoài nhà, nhu cầu Cloud và thời gian lưu. Đây là cơ sở chọn thiết bị và upload.'),
    ]
    cards = ''.join(f'<div class="editorial-card"><strong>{a}</strong><p>{b}</p></div>' for a,b in scenario_cards)
    faqs = [
        (f'Gói FPT nào phù hợp nhất tại {name}?', 'Không có một gói tốt nhất cho mọi địa chỉ. Hãy xác định số người, thiết bị, số tầng, nhu cầu upload, FPT Play, camera và ngân sách; sau đó mới đối chiếu catalog và kiểm tra hạ tầng tại địa chỉ.'),
        ('Có nên chọn gói cao nhất để Wi‑Fi mạnh hơn không?', 'Không nhất thiết. Băng thông đường truyền và vùng phủ Wi‑Fi là hai bài toán khác nhau. Nhà nhiều tầng thường cần bố trí Access Point/Mesh hợp lý, kể cả khi đường truyền đã nhanh.'),
        ('Khi nào nên ưu tiên META hoặc gói đối xứng?', 'Khi upload quan trọng: sao lưu cloud, gửi file lớn, livestream, làm việc với dữ liệu từ xa hoặc nhiều camera. Hãy so sánh cả download và upload thay vì chỉ nhìn tốc độ tải xuống.'),
        ('Wi‑Fi 7 có cần thiết cho mọi gia đình?', 'Không. Wi‑Fi 7 phù hợp khi có thiết bị tương thích, nhiều thiết bị đồng thời hoặc nhu cầu băng thông rất cao. Với nhu cầu phổ thông, Wi‑Fi 6 và bố trí điểm phát tốt có thể hợp lý hơn.'),
        ('Combo FPT Play khác Internet thuần ở đâu?', 'Combo thêm lớp giải trí/truyền hình và có thể đi kèm thiết bị/quyền lợi nội dung. Nếu gia đình không dùng FPT Play thường xuyên, hãy so tổng chi phí thay vì mặc định chọn combo.'),
        ('Lắp Camera cùng Internet cần hỏi gì?', 'Hỏi rõ model camera, số lượng, vị trí trong/ngoài nhà, Cloud, thời gian lưu, nguồn điện, đường truyền và chi phí phát sinh. Không nên chỉ nhìn giá thiết bị ban đầu.'),
        ('Giá trên trang có phải giá cố định cho toàn tỉnh/thành không?', 'Không. Catalog dùng để so sánh. Giá, thiết bị, ưu đãi và khả năng triển khai cần xác nhận theo địa chỉ và thời điểm trước khi đồng ý đăng ký.'),
        ('Cần chuẩn bị gì trước khi kỹ thuật đến?', 'Xác định vị trí modem, nơi đặt TV/PC/camera, ổ điện, khu vực cần Wi‑Fi mạnh và người có thể xác nhận phương án đi dây. Chuẩn bị trước giúp hạn chế đổi vị trí sau lắp đặt.'),
        ('Sau khi lắp nên kiểm tra những gì?', 'Kiểm tra kết nối tại vị trí sử dụng thật, thử thiết bị quan trọng, xác nhận tên Wi‑Fi/mật khẩu, thiết bị bàn giao, quyền lợi dịch vụ và cách yêu cầu hỗ trợ. Với nhà nhiều tầng, thử từng vùng thay vì đứng cạnh modem.'),
    ]
    faq_html = ''.join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q,a in faqs)

    return f'''<section class="local-editorial-v2" data-local-editorial-v2="true" data-local-focus="{escape(slug)}"><div class="container editorial-shell">
<div class="editorial-lead"><article class="editorial-intro"><span class="editorial-kicker">Cẩm nang chọn gói tại {escape(name)}</span><h2>Lắp mạng FPT tại {escape(name)}: chọn gói, thiết bị và phương án Wi‑Fi thế nào cho đúng?</h2><p>Trang này không chỉ liệt kê tên gói. Mục tiêu là giúp bạn biến nhu cầu thực tế thành một cấu hình có thể kiểm tra: cần bao nhiêu băng thông, upload có quan trọng không, nhà có cần Access Point/Mesh, có dùng FPT Play hay Camera, và điều gì phải xác nhận theo địa chỉ trước khi chốt.</p><p>{escape(focus)}</p><p>{escape(admin)}</p><ul class="editorial-admin-list">{admin_list}</ul></article>
<aside class="editorial-summary"><span class="editorial-kicker">Đọc nhanh trước khi chọn</span><h3>5 điều cần chốt</h3><ul><li>Nhu cầu thật và số thiết bị đồng thời.</li><li>Download, upload và độ trễ quan trọng đến mức nào.</li><li>Số tầng/phòng cần phủ Wi‑Fi.</li><li>Có cần FPT Play, Camera, IP tĩnh hoặc gói doanh nghiệp.</li><li>Giá, thiết bị và hạ tầng phải xác nhận theo địa chỉ.</li></ul></aside></div>
<div class="editorial-grid">
<article class="editorial-section full"><h3>1. Bắt đầu từ nhu cầu, không bắt đầu từ tên gói</h3><p>GIGA, SKY, META, F‑Game, SpeedX hay Lux/Super Biz chỉ có ý nghĩa khi chúng giải quyết đúng nhu cầu. Một gia đình chủ yếu xem video và học online khác với người livestream mỗi ngày; nhà một tầng khác nhà nhiều tầng; cửa hàng có camera và POS khác căn hộ chỉ dùng điện thoại, TV và laptop.</p><p>Trước khi hỏi “gói nào mạnh nhất”, hãy ghi lại số người dùng, số thiết bị kết nối đồng thời, thiết bị nào là quan trọng, diện tích/số tầng cần phủ Wi‑Fi, nhu cầu tải file lên cloud, camera và nội dung FPT Play. Danh sách này giúp loại bỏ nhanh những gói quá thấp hoặc quá cao so với thực tế.</p><div class="editorial-table-wrap"><table><thead><tr><th>Hồ sơ sử dụng</th><th>Điểm cần quan tâm</th><th>Cách chọn</th></tr></thead><tbody>{rows}</tbody></table></div></article>
<article class="editorial-section"><h3>2. Internet thuần, FPT Play hay Internet + Camera?</h3><p><strong>Internet thuần</strong> phù hợp khi mục tiêu chính là kết nối. <strong>Combo FPT Play</strong> đáng xem khi gia đình thực sự dùng truyền hình, phim hoặc thể thao. <strong>Internet + Camera</strong> phù hợp khi muốn gom đường truyền và giám sát trong cùng hệ sinh thái. Với cửa hàng/văn phòng, nhóm <strong>Lux/Super Biz</strong> nên được so riêng thay vì ép nhu cầu nghiệp vụ vào gói gia đình.</p><p>Đừng so chỉ giá tháng đầu. Hãy so tổng quyền lợi, thiết bị, dịch vụ đi kèm và phần nào bạn thực sự sử dụng. Một combo rẻ hơn trên giấy nhưng có quyền lợi không dùng đến chưa chắc tối ưu.</p></article>
<article class="editorial-section"><h3>3. Download và upload: nhìn cả hai chiều</h3><p>Download ảnh hưởng tải web, xem video và nhận dữ liệu. Upload quan trọng khi họp trực tuyến, gửi file lớn, sao lưu cloud, livestream và camera. Nếu chỉ nhìn một con số tốc độ lớn ở chiều download, bạn có thể bỏ qua đúng yếu tố gây nghẽn trong công việc hằng ngày.</p><p>Với người làm nội dung, studio nhỏ, camera nhiều hoặc làm việc từ xa thường xuyên, nhóm băng thông đối xứng như META hoặc các gói cao cấp có thể đáng so sánh hơn. Quyết định cuối vẫn phải dựa vào thiết bị và hạ tầng thực tế tại địa chỉ.</p></article>
<article class="editorial-section full"><h3>4. Nhà nhiều tầng: tốc độ cao không thay thế được vùng phủ</h3><p>Wi‑Fi suy giảm theo khoảng cách, vật cản và cách bố trí điểm phát. Vì vậy, nhà nhiều tầng nên tách bài toán thành hai lớp: đường truyền đến modem và vùng phủ từ modem/Access Point/Mesh đến từng phòng. Nếu tầng trên yếu, nâng gói từ vài trăm Mbps lên vài Gbps nhưng không thay đổi điểm phát có thể không giải quyết nguyên nhân.</p><div class="editorial-cards">{cards}</div><div class="editorial-callout"><strong>Nguyên tắc thực dụng:</strong> thiết bị quan trọng như PC làm việc, máy chơi game, NAS hoặc đầu ghi nên ưu tiên kết nối dây khi khả thi; Wi‑Fi dành cho tính linh hoạt, còn Mesh/Access Point dùng để mở rộng vùng phủ có chủ đích.</div></article>
<article class="editorial-section"><h3>5. Wi‑Fi 6, Wi‑Fi 7 và XGS‑PON: khi nào nên nâng cấp?</h3><p>Wi‑Fi 6 phù hợp với phần lớn thiết bị phổ thông hiện nay. Wi‑Fi 7 và nhóm SpeedX đáng cân nhắc khi bạn có thiết bị tương thích, nhiều người dùng đồng thời, truyền dữ liệu cục bộ lớn hoặc muốn đầu tư hạ tầng dài hạn. XGS‑PON tạo nền cho các gói 2–10 Gbps, nhưng tốc độ thực tế tới từng thiết bị còn phụ thuộc cổng mạng, Wi‑Fi, dây, máy khách và cách bố trí.</p><p>Do đó, không nên mua Wi‑Fi 7 chỉ vì tên công nghệ. Hãy kiểm tra thiết bị đang có, thiết bị dự kiến mua và nhu cầu thực tế trong 12–24 tháng tới.</p></article>
<article class="editorial-section"><h3>6. Gaming và livestream: ưu tiên độ trễ, upload và đường đi tín hiệu</h3><p>Game online cần độ trễ ổn định hơn là chỉ cần tốc độ tải cực cao. Livestream cần upload bền vững. Nếu phòng game xa modem, hãy xử lý kết nối dây hoặc điểm phát trước. Nhóm F‑Game có thể hữu ích khi bạn muốn tính năng tối ưu game, nhưng vẫn cần kiểm tra tuyến kết nối trong nhà và điều kiện thực tế.</p><p>Khi tư vấn, hãy nói rõ game/ứng dụng thường dùng, có stream không, máy kết nối LAN hay Wi‑Fi và trong nhà có bao nhiêu thiết bị hoạt động cùng lúc.</p></article>
<article class="editorial-section full"><h3>7. Checklist chi phí trước khi ký</h3><p>Một “giá cước/tháng” chưa phải toàn bộ chi phí. Trước khi xác nhận tại {escape(name)}, hãy yêu cầu tách rõ các thành phần dưới đây để có thể so các phương án trên cùng mặt bằng.</p><ul class="editorial-checklist"><li>Giá cước định kỳ và VAT.</li><li>Phí lắp đặt/hòa mạng nếu có.</li><li>Modem, Access Point hoặc Mesh đi kèm.</li><li>FPT Play Box hoặc quyền lợi nội dung.</li><li>Camera, Cloud và thời gian lưu.</li><li>Điều kiện trả trước/chu kỳ thanh toán.</li><li>Ưu đãi có ngày hết hạn hoặc điều kiện kèm theo.</li><li>Chi phí phát sinh khi đổi vị trí/nâng cấp thiết bị.</li></ul><div class="editorial-callout">Mức giá hiển thị trong catalog bên dưới là dữ liệu so sánh theo snapshot. FPT cũng nêu giá có thể thay đổi theo khu vực và thời điểm; vì vậy báo giá cuối phải được xác nhận theo địa chỉ.</div></article>
<article class="editorial-section"><h3>8. Địa chỉ tại {escape(name)}: ghi sao để kiểm tra không nhầm?</h3><p>{escape(admin)}</p><p>Định dạng hữu ích là: <strong>xã/phường hiện hành → đường/khu vực → số nhà hoặc mốc gần vị trí lắp → tên tỉnh cũ nếu có</strong>. Nếu là căn hộ, thêm tên tòa và tầng; nếu là cơ sở kinh doanh, thêm tên cửa hàng và vị trí cần đặt modem.</p></article>
<article class="editorial-section"><h3>9. Chọn vị trí modem trước khi kỹ thuật đến</h3><p>Vị trí modem nên gần trung tâm vùng sử dụng, thông thoáng, có nguồn điện và thuận tiện đi dây tới thiết bị quan trọng. Tránh chốt vị trí chỉ vì “gần cửa” nếu khu vực dùng Wi‑Fi chính nằm sâu bên trong. Với nhà nhiều tầng, nên xác định trước nơi đặt Access Point/Mesh và đường đi dây giữa các tầng.</p><p>Một sơ đồ đơn giản vẽ các phòng, TV, PC và camera thường giúp tư vấn nhanh hơn nhiều so với mô tả bằng cảm giác “nhà hơi rộng”.</p></article>
<article class="editorial-section full"><h3>10. Quy trình 8 bước từ nhu cầu đến nghiệm thu</h3><ol class="editorial-steps"><li><strong>Ghi nhu cầu.</strong> Liệt kê người dùng, thiết bị, game, TV, camera và công việc.</li><li><strong>Ghi địa chỉ.</strong> Dùng xã/phường hiện hành, mốc vị trí và tên cũ nếu cần.</li><li><strong>Chọn nhóm gói.</strong> Internet, FPT Play, Camera, Wi‑Fi 7 hay doanh nghiệp.</li><li><strong>So cấu hình.</strong> Đặt download, upload, thiết bị và giá cạnh nhau.</li><li><strong>Kiểm tra hạ tầng.</strong> Chỉ chốt khi địa chỉ thực tế được xác minh.</li><li><strong>Chốt thiết bị.</strong> Xác nhận modem, AP/Mesh, Box, camera và Cloud.</li><li><strong>Chốt tổng chi phí.</strong> Tách phí định kỳ, lắp đặt và điều kiện ưu đãi.</li><li><strong>Nghiệm thu thực tế.</strong> Thử tại các phòng/tầng và thiết bị quan trọng.</li></ol></article>
<article class="editorial-section"><h3>11. Sau khi lắp: kiểm tra bằng tình huống thật</h3><p>Đừng chỉ đứng cạnh modem chạy speed test. Hãy thử đúng nơi thường dùng: bàn làm việc, phòng ngủ, TV, phòng game, quầy bán hàng và vị trí camera. Thử cả giờ có nhiều thiết bị hoạt động nếu có thể. Nếu một vùng yếu, xác định đó là vấn đề vùng phủ, thiết bị hay đường truyền trước khi đổi gói.</p><p>Ghi lại tên thiết bị được bàn giao, vị trí lắp, tài khoản ứng dụng liên quan và kênh hỗ trợ. Việc này giúp xử lý sự cố sau này nhanh hơn.</p></article>
<article class="editorial-section"><h3>12. 6 lỗi chọn gói thường gặp</h3><ul><li>Chọn theo giá thấp nhất nhưng không tính số tầng và thiết bị.</li><li>Chọn theo download nhưng bỏ qua upload.</li><li>Nâng băng thông để chữa một điểm Wi‑Fi yếu.</li><li>Nhận combo có nhiều quyền lợi nhưng không dùng.</li><li>Không hỏi rõ số lượng/model thiết bị đi kèm.</li><li>Chốt giá trước khi địa chỉ và chương trình ưu đãi được xác nhận.</li></ul></article>
</div>
<div class="editorial-faq"><span class="editorial-kicker">FAQ thực tế</span><h3>13. Câu hỏi thường gặp khi chọn gói FPT tại {escape(name)}</h3>{faq_html}</div>
<div class="editorial-cta"><div><h3>Đã rõ nhu cầu? So catalog đầy đủ ngay bên dưới</h3><p>Chọn gói trước, sau đó gửi địa chỉ để kiểm tra khả dụng, thiết bị và giá cuối.</p></div><a class="btn btn-primary" href="#goi-dich-vu-dia-phuong">Xem toàn bộ gói cước</a></div>
<p class="editorial-muted">Nội dung hướng dẫn không khẳng định hạ tầng hay ưu đãi cho toàn {escape(name)}. Thông tin thương mại cần xác nhận theo địa chỉ và thời điểm.</p>
</div></section>'''


def inject(path: Path, loc: dict, idx: int) -> None:
    html = path.read_text(encoding='utf-8')
    if 'data-local-editorial-v2=' in html:
        raise SystemExit(f'LOCAL EDITORIAL BUILD FAIL: duplicate editorial in {path}')
    marker = '<section class="section local-commerce" id="goi-dich-vu-dia-phuong"'
    if marker not in html:
        raise SystemExit(f'LOCAL EDITORIAL BUILD FAIL: commerce marker missing in {path}')
    html = html.replace(marker, section(loc, idx) + marker, 1)
    css = '<link rel="stylesheet" href="../../assets/css/local-editorial-v2.css" data-local-editorial-v2-style="true"/>'
    if 'data-local-editorial-v2-style=' not in html:
        html = html.replace('</head>', css + '</head>', 1)
    path.write_text(html, encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True)
    parser.add_argument('--locations-script', default='scripts/generate-local-pages.py')
    args = parser.parse_args()
    locations = load_locations(Path(args.locations_script))
    if len(locations) != 34:
        raise SystemExit(f'LOCAL EDITORIAL BUILD FAIL: expected 34 locations, got {len(locations)}')
    if set(FOCUS) != {x['slug'] for x in locations}:
        raise SystemExit('LOCAL EDITORIAL BUILD FAIL: local focus map does not match 34 locations')
    site = Path(args.site)
    for idx, loc in enumerate(locations):
        path = site / 'khu-vuc' / loc['slug'] / 'index.html'
        if not path.exists():
            raise SystemExit(f"LOCAL EDITORIAL BUILD FAIL: missing {loc['slug']}")
        inject(path, loc, idx)
    print('LOCAL EDITORIAL BUILT: 34/34 province pages upgraded with longform buying guide, decision matrix, cost checklist, install workflow, 9 FAQ and unique local/admin context')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
