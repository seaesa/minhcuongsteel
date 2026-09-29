"""Generates index.html from section templates + data lists."""
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://minhcuongsteel.com"

ARROW_RIGHT = '<svg class="ic-angle-right" viewBox="0 0 8 14" width="7" height="12" aria-hidden="true"><path d="M1 1l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ANGLE_DOWN = '<svg class="ic-angle-down" viewBox="0 0 12 8" width="10" height="7" aria-hidden="true"><path d="M1 1.5l5 5 5-5" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SEARCH = '<svg class="ic-search" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M10.5 3a7.5 7.5 0 015.96 12.06l4.24 4.23a1 1 0 01-1.42 1.42l-4.23-4.24A7.5 7.5 0 1110.5 3zm0 2.2a5.3 5.3 0 100 10.6 5.3 5.3 0 000-10.6z" fill="currentColor"/></svg>'

def e(s):
    return html.escape(s, quote=True)

NAV = [
    ("Giới thiệu", f"{SITE}/gioi-thieu/", []),
    ("Sản phẩm &amp; Dịch vụ", f"{SITE}/dich-vu", [
        ("Kết cấu thép – Tôn lợp", f"{SITE}/dich-vu/ket-cau-thep-ton-lop/"),
        ("Lưới thép hàn – Xà gồ", f"{SITE}/dich-vu/luoi-thep-han/"),
        ("Tư vấn thiết kế", f"{SITE}/dich-vu/tu-van-thiet-ke/"),
        ("Kinh doanh thép", f"{SITE}/dich-vu/kinh-doanh-thep/"),
        ("Thi công – lắp dựng", f"{SITE}/dich-vu/long-thep-tru-hang/"),
        ("Dịch vụ Cẩu – Vận tải", f"{SITE}/dich-vu/dich-vu-cau-van-tai/"),
        ("Sản phẩm khác", f"{SITE}/dich-vu/san-pham-khac/"),
    ]),
    ("Dự án", f"{SITE}/du-an", [
        ("Dự án Nước ngoài", f"{SITE}/du-an/du-an-nuoc-ngoai/"),
        ("Dự án Trong nước", f"{SITE}/du-an/du-an-trong-nuoc/"),
    ]),
    ("Tin tức", "#", [
        ("Tin tức", f"{SITE}/tin-tuc/"),
        ("Tuyển dụng", f"{SITE}/tuyen-dung/"),
        ("Thông báo Nhân Sự", f"{SITE}/tin-tuc/thong-bao-nhan-su/"),
    ]),
    ("Liên hệ", f"{SITE}/lien-he/", []),
]

LANGS = [("zh-CN", "Chinese (Simplified)"), ("en", "English"), ("ja", "Japanese"), ("vi", "Vietnamese")]

HERO_TEXT = "Là thương hiệu Công ty cổ phần Cơ khí – Xây lắp – Thương mại Minh Cường, có thâm niên hơn {n} năm hoạt động lĩnh vực xây dựng nhà tiền chế, kết cấu thép, xây dựng, cơ khí ở Việt Nam."

NEWS = [
    ("Minh Cường Steel tham gia Ngày hội gắn kết giáo dục nghề nghiệp Thủ đô với thị trường lao động năm 2026", "21/04/2026",
     "Minh Cường Steel đã tích cực tham gia Ngày hội gắn kết giáo dục nghề nghiệp Thủ đô với thị trường lao...", "news-1.jpg",
     "/minh-cuong-steel-tham-gia-ngay-hoi-gan-ket-giao-duc-nghe-nghiep-thu-do-voi-thi-truong-lao-dong-nam-2026/"),
    ("Ra quân đầu xuân quyết tâm hoàn thành mục tiêu sxkd năm 2026", "24/02/2026",
     "Trong không khí phấn khởi khai xuân những ngày đầu năm mới, Công ty  vinh dự được đón tiếp: Đ/c Lê Đình Hùng – Ủy...", "news-2.jpg",
     "/ra-quan-dau-xuan-quyet-tam-hoan-thanh-muc-tieu-sxkd-nam-2026/"),
    ("Minh Cường Steel tham gia Hội thi Thợ giỏi Thành phố Hà Nội năm 2025", "28/10/2025",
     "Minh Cường Steel tham gia Hội thi Thợ giỏi Thành phố Hà Nội với mục tiêu không chỉ nâng cao tay nghề và tôn vinh...", "news-3.jpg",
     "/minh-cuong-steel-tham-gia-hoi-thi-tho-gioi-thanh-pho-ha-noi-nam-2025/"),
    ("Minh Cường Steel chung tay hỗ trợ cbcnv bị ảnh hưởng bão lũ", "13/10/2025",
     "Trong những ngày qua, cơn bão số 11 (Matmo) cùng việc xả lũ từ thượng nguồn đã gây ngập lụt tại nhiều khu vực sinh...", "news-4.jpg",
     "/minh-cuong-steel-chung-tay-ho-tro-cbcnv-bi-anh-huong-bao-lu/"),
    ("Giải Golf kỷ niệm 28 năm thành lập Minh Cường Steel", "26/08/2025",
     "GIẢI GOLF KỶ NIỆM 28 NĂM THÀNH LẬP MINH CƯỜNG STEEL ⛳🎉 📅 Ngày 24/8/2025, Công Ty CP Cơ Khí Xây Lắp...", "news-5.png",
     "/giai-golf-ky-niem-28-nam-thanh-lap-minh-cuong-steel/"),
    ("Khám phá nhà máy cơ khí cùng các em học sinh trường Alpha", "23/05/2025",
     "Công ty CP Cơ khí – Xây lắp – Thương mại Minh Cường hân hạnh được chào đón các em học sinh...", "news-6.jpg",
     "/kham-pha-nha-may-co-khi-cung-cac-em-hoc-sinh-truong-alpha/"),
    ("Minh Cường Steel trao quà Tết cho học sinh nghèo học giỏi, con gia đình chính sách tại Xã Dục Tú", "21/01/2025",
     "Hưởng ứng chương trình: “Xuân chung tay đoàn kết, Tết thắm tình quân dân” của Ban Chỉ huy quân sự huyện Đông...", "news-7.jpg",
     "/minhc-cuong-steel-trao-qua-tet-cho-hoc-sinh-ngheo-hoc-gioi-con-gia-dinh-chinh-sach-tai-xa-duc-tu/"),
    ("Huấn luyện an toàn vệ sinh lao động năm 2024", "29/10/2024",
     "Minh Cường steel tổ chức huấn luyện an toàn vệ sinh lao động (ATVSLĐ) định kỳ năm 2024 cho CBCNV. Huấn luyện...", "news-8.jpg",
     "/huan-luyen-an-toan-ve-sinh-lao-dong-nam-2024/"),
]

PRODUCTS = [
    ("Kết cấu thép - Tôn lợp", "product-ketcauthep.jpg", "/dich-vu/ket-cau-thep-ton-lop/"),
    ("Lưới thép hàn - Xà gồ", "product-luoithep.jpg", "/dich-vu/luoi-thep-han/"),
    ("Tư vấn thiết kế", "product-tuvanthietke.jpg", "/dich-vu/tu-van-thiet-ke/"),
    ("Kinh doanh thép", "product-kinhdoanhthep.jpg", "/dich-vu/kinh-doanh-thep/"),
    ("Thi công - lắp dựng", "product-thicong.png", "/dich-vu/long-thep-tru-hang/"),
    ("Dịch vụ Cẩu - Vận tải", "product-vantai.jpg", "/dich-vu/dich-vu-cau-van-tai/"),
    ("Sản phẩm khác", "product-khac.png", "/dich-vu/san-pham-khac/"),
]

PROJECTS_ND = [
    ("Dự án nhà máy giấy bao bì công nghệ cao GĐT", "/du-an/du-an-nha-may-giay-bao-bi-cong-nghe-cao-gdt/"),
    ("Dự án thép Việt Úc – Vinausteel", "/du-an/du-an-thep-viet-uc-vinausteel/"),
    ("Công trình Mặt Trời Kinh Bắc – Bắc Ninh", "/du-an/cong-trinh-mat-troi-kinh-bac-bac-ninh/"),
    ("Nhà ga T2 sân bay Nội Bài", "/du-an/nha-ga-t2-san-bay-noi-bai/"),
    ("Dự án Hòa Phát Dung Quất 2", "/du-an/du-an-hoa-phat-dung-quat-2-2/"),
    ("Tổng hợp các dự án kết cấu thép nổi bật của Minh Cường Steel", "/du-an/tong-hop-cac-du-an-ket-cau-thep-noi-bat-cua-minh-cuong-steel/"),
    ("Điểm danh các dự án trong nước ấn tượng được triển khai bởi Minh Cường Steel", "/du-an/diem-danh-cac-du-an-trong-nuoc-an-tuong-duoc-trien-khai-boi-minh-cuong-steel/"),
    ("Dự án Phân xưởng Nguyên Liệu – Nhà máy Luyện Cốc – Dự án Hòa Phát Dung Quất 2", "/du-an/du-an-hoa-phat-dung-quat-2/"),
    ("Dự án Xây dựng Xí nghiệp liên hợp giết mổ sạch của Daesang Đức Việt", "/du-an/xi-nghiep-lien-hop-giet-mo-sach/"),
    ("Dự án Phát triển kho hàng Bắc Ninh – Công ty TNHH Welvista", "/du-an/phat-trien-kho-hang-bac-ninh/"),
    ("Dự án Xây dựng nhà kho Công ty TNHH HuaYuan Machinery tại Hải Phòng", "/du-an/xay-dung-nha-kho-huayuan-machinery/"),
    ("Dự án Nhà máy sản xuất máy biến áp, tủ bảng điện – Công ty HBT", "/du-an/nha-may-san-xuat-may-bien-ap/"),
]
PROJECTS_XK = [
    ("Dự án Công ty TNHH thực phẩm ORION Vina", "/du-an/"),
    ("Dự án Interflex Vina", "/du-an/"),
    ("Nhà máy sản xuất bao bì giấy và đồ nhựa Depak", "/du-an/"),
    ("Dự Án LG Electronics", "/du-an/"),
    ("Jeil Logistics Hải Phòng", "/du-an/"),
    ("Dự án Woonyoung Vina", "/du-an/"),
    ("Dự án LG Innotek V3 Project", "/du-an/"),
    ("Top các dự án nước ngoài nổi bật khác được triển khai bởi Minh Cường Steel", "/du-an/"),
    ("Minh Cường Steel xuất khẩu thành công Ván khuôn &amp; Đà giáo sang thị trường Singapore", "/du-an/"),
    ("Xuất khẩu thành công Ván khuôn xà mũ và Ván khuôn cột sang thị trường Australia", "/du-an/van-khuon-xa-mu-van-khuon-cot/"),
    ("Dự án công ty tnhh Welvista", "/du-an/du-an-cong-ty-tnhh-welvista/"),
    ("Nhà máy HuaYuan Machinery Việt Nam", "/du-an/nha-may-huayuan-machinery-viet-nam/"),
]

# Why-choose-us panels: original copy, same structure as the live site's panels.
WHY = [
    ("chat-luong", "Chất lượng", "icon-chatluong.png", """<p>Với chúng tôi, chất lượng không dừng ở sản phẩm cuối cùng mà bắt đầu từ khâu chọn thép, gia công đến lắp dựng tại công trường. Mỗi cấu kiện đều được kiểm tra theo từng công đoạn, có hồ sơ nghiệm thu rõ ràng, để khách hàng yên tâm về độ bền và tuổi thọ công trình. Cam kết đó được thể hiện qua:</p>
<ul><li>Nguồn vật liệu đạt chuẩn, có chứng chỉ xuất xưởng</li><li>Gia công chính xác trên dây chuyền hiện đại</li><li>Kiểm tra mối hàn và kích thước theo từng lô</li><li>Quy trình nghiệm thu minh bạch, đầy đủ hồ sơ</li><li>Bảo hành rõ ràng sau bàn giao</li><li>Sẵn sàng đáp ứng yêu cầu kỹ thuật riêng</li></ul>"""),
    ("an-toan", "An toàn ", "icon-antoan.png", """<p>An toàn là điều kiện tiên quyết trong mọi hoạt động của Minh Cường Steel. Từ xưởng sản xuất đến công trường, chúng tôi áp dụng quy trình kiểm soát rủi ro chặt chẽ, trang bị đầy đủ bảo hộ cho người lao động và chỉ bàn giao những kết cấu đã được kiểm định an toàn cho người sử dụng.</p>
<p>Những nguyên tắc chúng tôi luôn tuân thủ:</p>
<ul><li>Đánh giá rủi ro trước khi thi công</li><li>Huấn luyện an toàn lao động định kỳ</li><li>Thiết bị nâng hạ được kiểm định đầy đủ</li><li>Xử lý kịp thời mọi sự cố phát sinh</li><li>Hạn chế tối đa tác động đến môi trường</li></ul><p>&nbsp;</p>"""),
    ("trach-nhiem", "Trách nhiệm", "icon-trachnhiem.png", """<p>Chúng tôi làm việc với tinh thần chịu trách nhiệm đến cùng cho từng hạng mục đã nhận, từ bản vẽ thiết kế đến khi công trình đi vào sử dụng. Mọi phản hồi của khách hàng đều được tiếp nhận nhanh và xử lý dứt điểm.</p>
<ul><li>Đồng hành cùng khách hàng từ tư vấn đến bàn giao</li><li>Phản hồi và hỗ trợ kỹ thuật nhanh chóng</li><li>Linh hoạt điều chỉnh theo nhu cầu thực tế</li><li>Giải quyết khiếu nại công bằng, thấu đáo</li><li>Đóng góp tích cực cho cộng đồng và xã hội</li></ul>"""),
    ("uy-tin", "Uy tín", "icon-uytin.png", """<p>Uy tín của Minh Cường Steel được xây dựng từ hàng trăm công trình trong nước và xuất khẩu qua gần ba thập kỷ hoạt động. Khách hàng và đối tác tiếp tục lựa chọn chúng tôi vì:</p>
<ul><li>Kinh nghiệm dày dạn trong lĩnh vực kết cấu thép</li><li>Nói đi đôi với làm, giữ đúng thỏa thuận</li><li>Chất lượng được kiểm chứng qua từng dự án</li><li>Quan hệ hợp tác lâu dài, tin cậy</li></ul>"""),
    ("chuyen-nghiep", "Chuyên nghiệp", "icon-chuyennghiep.png", """<p>Đội ngũ kỹ sư thiết kế, giám sát và thợ lành nghề của chúng tôi được đào tạo bài bản, thường xuyên cập nhật công nghệ và tiêu chuẩn mới. Mỗi thành viên hiểu rõ vai trò của mình trong chuỗi công việc, giúp sản phẩm đạt độ chính xác cao và đồng đều.</p>
<p>Các dự án được quản lý theo kế hoạch chi tiết, phân công rõ ràng và báo cáo tiến độ định kỳ cho chủ đầu tư. Chúng tôi coi trọng sự minh bạch trong trao đổi, chi phí và chất lượng, bởi đó là nền tảng để mỗi dự án kết thúc suôn sẻ và mở ra cơ hội hợp tác tiếp theo.</p>"""),
    ("ky-luat", "Kỷ luật", "icon-kyluat.png", """<p>Kỷ luật giúp chúng tôi giữ vững cam kết về thời gian: tiến độ đã thống nhất với khách hàng được xem là mốc bắt buộc phải hoàn thành, không phải mục tiêu tham khảo.</p>
<p>Mọi công đoạn đều vận hành theo quy trình chuẩn, có người phụ trách và điểm kiểm soát cụ thể. Hiệu suất và tiến độ được rà soát thường xuyên để phát hiện sớm vướng mắc và điều chỉnh kịp thời.</p>
<p>Nhờ đó, khách hàng có thể chủ động kế hoạch của mình khi làm việc cùng Minh Cường Steel.</p>"""),
]

PARTNERS = sorted(p.name for p in (ROOT / "images/partners").iterdir())

FOOTER_SERVICES = [
    ("Kết cấu thép &amp; tôn lợp", "/dich-vu/ket-cau-thep-ton-lop/"), ("Lưới thép hàn - Xà gồ", "/dich-vu/luoi-thep-han/"),
    ("Tư vấn thiết kế", "/dich-vu/tu-van-thiet-ke/"), ("Kinh doanh thép", "/dich-vu/kinh-doanh-thep/"),
    ("Thi công - lắp dựng", "/dich-vu/long-thep-tru-hang/"), ("Dịch vụ cẩu - vận tải", "/dich-vu/dich-vu-cau-van-tai/"),
    ("Sản phẩm khác", "/dich-vu/san-pham-khac/"),
]
FOOTER_INFO = [("Giới thiệu", "/gioi-thieu/"), ("Dự án", "/du-an"), ("Tin tức", "/tin-tuc/"), ("Tuyển dụng", "/tuyen-dung/"), ("Liên hệ", "/lien-he/")]
SOCIAL = [
    ("facebook.svg", "https://www.facebook.com/minhcuongsteel.vn/?ref=embed_page", "Facebook", 50),
    ("youtube.svg", "https://www.youtube.com/@minhcuongsteel9241", "Youtube", 50),
    ("zalo.png", "https://zalo.me/0936078586", "Zalo", 40),
    ("linkedin.png", "https://www.linkedin.com/company/minh-cuong-mechanics-construction-trading-joint-stock-company/", "LinkedIn", 40),
    ("whatsapp.png", "https://wa.me/+84988459353", "WhatsApp", 40),
]


def title(text, extra=""):
    return f'<div class="title{extra}" data-animate="fadeInUp"><h2>{text}</h2></div>'


def desktop_nav():
    out = []
    for label, href, subs in NAV:
        if subs:
            items = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in subs)
            out.append(f'<li class="menu-item has-dropdown"><a class="nav-top-link" href="{href}">{label}{ANGLE_DOWN}</a><ul class="nav-dropdown">{items}</ul></li>')
        else:
            out.append(f'<li class="menu-item"><a class="nav-top-link" href="{href}">{label}</a></li>')
    return "".join(out)


def mobile_nav():
    out = []
    for label, href, subs in NAV:
        if subs:
            items = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in subs)
            out.append(f'<li class="menu-item has-child"><a href="{href}">{label}</a><button class="toggle" aria-label="Toggle">{ANGLE_DOWN}</button><ul class="sub-menu">{items}</ul></li>')
        else:
            out.append(f'<li class="menu-item"><a href="{href}">{label}</a></li>')
    return "".join(out)


def lang_switcher(extra=""):
    opts = "".join(f'<a href="#" data-lang="{c}" title="{n}"{" class=\"gt-current\"" if c == "vi" else ""}><img src="images/flags/{c}.svg" width="24" height="24" alt="{c}"></a>' for c, n in LANGS)
    return f'<div class="gt-switcher{extra}"><button class="gt-selected" type="button" aria-label="Chọn ngôn ngữ"><img src="images/flags/vi.svg" width="24" height="24" alt="vi"><span class="gt-arrow"></span></button><div class="gt-options">{opts}</div></div>'


def hero_desktop():
    slides = []
    for i in range(13):
        n = 28 if i == 0 else 26
        slides.append(f'''<section class="hero-slide{' is-selected' if i == 0 else ''}" data-bg="images/hero/hero-{i + 1}.jpg"{f' style="background-image:url(images/hero/hero-1.jpg)"' if i == 0 else ''}>
  <div class="hero-row"><div class="hero-col" data-animate="fadeInRight"><div class="hero-inner">
    <h2>MINH CUONG</h2><h3>Steel</h3>
    <p>{HERO_TEXT.format(n=n)}</p>
    <a href="{SITE}/gioi-thieu/" class="button primary btn-main"><span>Xem chi tiết</span>{ARROW_RIGHT}</a>
  </div></div></div>
</section>''')
    return "\n".join(slides)


def hero_mobile():
    return "\n".join(f'''<section class="hero-slide{' is-selected' if i == 0 else ''}" style="background-image:url(images/hero/hero-mobile.jpg)">
  <div class="hero-row"><div class="hero-col" data-animate="fadeInRight"><div class="hero-inner">
    <h2>MINH CUONG Steel</h2>
    <a href="{SITE}/gioi-thieu/" class="button primary btn-main"><span>Xem chi tiết</span>{ARROW_RIGHT}</a>
  </div></div></div>
</section>''' for i in range(2))


def post(p, kind):
    t, d, ex, img, href = p
    return f'''<div class="post-item {kind}"><a class="post-box" href="{SITE}{href}">
  <div class="post-image image-zoom"><img src="images/news/{img}" alt="{e(t)}" loading="lazy"></div>
  <div class="post-text"><h5 class="post-title">{t}</h5><div class="post-meta">{d}</div><p class="post-excerpt">{ex}</p></div>
</a></div>'''


def news():
    left = post(NEWS[0], "post-large")
    right = "".join(post(p, "post-small") for p in NEWS[1:4])
    slider = "".join(post(p, "post-slide") for p in NEWS)
    return left, right, slider


def products():
    return "".join(f'''<div class="ser-col"><div class="ser-box">
  <a class="ser-image image-zoom" href="{SITE}{h}"><img src="images/{img}" alt="{e(t)}" loading="lazy"></a>
  <div class="ser-text"><h3><a href="{SITE}{h}">{t}</a></h3></div>
</div></div>''' for t, img, h in PRODUCTS)


def projects(data, prefix):
    return "".join(f'''<div class="project-slide"><div class="project-inner"><div class="box-project">
  <div class="project-image"><img src="images/projects/{prefix}-{i + 1}.jpg" alt="{e(t)}" loading="lazy"></div>
  <div class="project-text"><div class="project-text-inner"><p>{t}</p>
    <a href="{SITE}{h}" class="button primary btn-main cus-arr-white"><span>Xem chi tiết</span><i class="arr"></i></a></div></div>
</div></div></div>''' for i, (t, h) in enumerate(data))


def why():
    tabs = []
    for i, (key, label, icon, body) in enumerate(WHY):
        act = " active" if i == 0 else ""
        tabs.append(f'''<div class="why-col"><div class="icon-tab{act}" data-tab="{key}" role="button" tabindex="0">
  <div class="icon-tab-img"><img src="images/{icon}" alt="" width="37" height="39"></div>
  <div class="icon-tab-text"><p>{label}</p></div>
</div><div class="icon-content{act}" id="why-{key}">{body}</div></div>''')
    return "".join(tabs)


def partners():
    return "".join(f'<div class="gallery-col" data-animate="bounceInUp"><div class="gallery-box image-zoom"><img src="images/partners/{p}" alt="Đối tác" loading="lazy"></div></div>' for p in PARTNERS)


def footer_links(items):
    return "".join(f'<a class="footer-link" href="{SITE}{h}"><span>{l}</span></a>' for l, h in items)


def social():
    return "".join(f'<a class="ux-logo" href="{h}" target="_blank" rel="noopener" aria-label="{a}"><img src="images/social/{f}" alt="{a}" style="height:{ht}px"></a>' for f, h, a, ht in SOCIAL)


left, right, slider = news()

page = (ROOT / "scripts/template.html").read_text(encoding="utf-8")
replacements = {
    "{{DESKTOP_NAV}}": desktop_nav(),
    "{{MOBILE_NAV}}": mobile_nav(),
    "{{LANG}}": lang_switcher(),
    "{{LANG_MOBILE}}": lang_switcher(" in-sidebar"),
    "{{HERO_DESKTOP}}": hero_desktop(),
    "{{HERO_MOBILE}}": hero_mobile(),
    "{{NEWS_LEFT}}": left,
    "{{NEWS_RIGHT}}": right,
    "{{NEWS_SLIDER}}": slider,
    "{{PRODUCTS}}": products(),
    "{{PROJECTS_ND}}": projects(PROJECTS_ND, "noi-dia"),
    "{{PROJECTS_XK}}": projects(PROJECTS_XK, "xuat-khau"),
    "{{WHY}}": why(),
    "{{PARTNERS}}": partners(),
    "{{FOOTER_SERVICES}}": footer_links(FOOTER_SERVICES),
    "{{FOOTER_INFO}}": footer_links(FOOTER_INFO),
    "{{SOCIAL}}": social(),
    "{{ARROW_RIGHT}}": ARROW_RIGHT,
    "{{SEARCH}}": SEARCH,
    "{{ANGLE_DOWN}}": ANGLE_DOWN,
    "{{TITLE_VIDEO}}": title("Video Về Chúng tôi", " gap-20"),
    "{{TITLE_NEWS}}": title("Tin Tức &amp; Sự Kiện"),
    "{{TITLE_PRODUCTS}}": title("Sản Phẩm Dịch Vụ"),
    "{{TITLE_PROJECTS}}": title("Dự án tiêu biểu"),
    "{{TITLE_WHY}}": title("Vì Sao Khách Hàng Chọn Chúng Tôi"),
    "{{TITLE_PARTNERS}}": title("Đối tác của chúng tôi"),
    "{{SITE}}": SITE,
}
for k, v in replacements.items():
    page = page.replace(k, v)
(ROOT / "index.html").write_text(page, encoding="utf-8")
print("index.html written", len(page))
