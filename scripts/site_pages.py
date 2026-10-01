"""Inner pages of the clone, rendered from data/site.json (see scrape_site.py).

Each builder returns a list of Page(path, title, body_class, nav, main_html).
build_html.py wraps them in the shared layout (header, footer, popups), fixes links
and writes <path>/index.html.
"""
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://minhcuongsteel.com"
DATA = json.loads((ROOT / "data/site.json").read_text(encoding="utf-8"))
IMAGES = json.loads((ROOT / "data/images.json").read_text(encoding="utf-8"))

PER_PAGE = 9


@dataclass
class Page:
    path: str
    title: str
    body_class: str
    nav: str          # top-level menu label to highlight
    main: str


def e(s):
    return html.escape(s or "", quote=True)


def img(url):
    """original upload URL -> local optimised copy (falls back to the original URL)"""
    if not url:
        return ""
    url = url.split("?")[0]
    return IMAGES.get(url) or IMAGES.get(url.replace("https://", "http://")) or IMAGES.get(url.replace("http://", "https://")) or url


def norm(path):
    """site path with exactly one trailing slash ('/du-an' -> '/du-an/')"""
    path = path.split("#")[0].split("?")[0]
    return path if path.endswith("/") else path + "/"


ICON_DATE = '<img class="icon_date" src="/images/theme/icon-date-v-2.png" alt="" width="18" height="20">'
CHEVRON = '<svg width="21" height="21" viewBox="0 0 21 21" fill="none" aria-hidden="true"><path d="M7.875 15.75L13.125 10.5L7.875 5.25" stroke="#444444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ANGLE = '<svg viewBox="0 0 8 14" width="8" height="14" aria-hidden="true"><path d="M1 1l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ANGLE_L = '<svg viewBox="0 0 8 14" width="8" height="14" aria-hidden="true"><path d="M7 1L1 7l6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SHARE_FB = '<a class="share-fb" href="https://www.facebook.com/sharer/sharer.php?u={u}" target="_blank" rel="noopener"><img src="/images/theme/share-fb.png" alt="Share on Facebook"></a>'


def date_html(d):
    return f'<div class="date_main_blog">{ICON_DATE}<div class="date_inner">{e(d)}</div></div>'


def crumbs(items, cls="breadcrumb"):
    parts = []
    for i, (label, href) in enumerate(items):
        if i:
            parts.append('<span class="separator"> / </span>')
        if href and i < len(items) - 1:
            parts.append(f'<a href="{href}">{e(label)}</a>')
        else:
            parts.append(f'<span class="last">{e(label)}</span>' if not href else f'<a href="{href}">{e(label)}</a>')
    return f'<nav class="{cls}" aria-label="breadcrumbs"><p>{"".join(parts)}</p></nav>'


def page_url(base, n):
    return base if n == 1 else f"{base}page/{n}/"


def pagination(base, cur, total, mid=2, cls="nav-pagination"):
    """WordPress paginate_links(): end_size 1, mid_size `mid`, prev/next arrows"""
    if total <= 1:
        return ""
    items, dots = [], False
    if cur > 1:
        items.append(f'<li><a class="prev page-number" href="{page_url(base, cur - 1)}" aria-label="Trang trước">{ANGLE_L}</a></li>')
    for n in range(1, total + 1):
        if n == cur:
            items.append(f'<li><span aria-current="page" class="page-number current">{n}</span></li>')
            dots = False
        elif n <= 1 or n > total - 1 or abs(n - cur) <= mid:
            items.append(f'<li><a class="page-number" href="{page_url(base, n)}">{n}</a></li>')
            dots = False
        elif not dots:
            items.append('<li><span class="page-number dots">…</span></li>')
            dots = True
    if cur < total:
        items.append(f'<li><a class="next page-number" href="{page_url(base, cur + 1)}" aria-label="Trang sau">{ANGLE}</a></li>')
    return f'<ul class="{cls}">{"".join(items)}</ul>'


def chunks(seq, n):
    return [seq[i:i + n] for i in range(0, len(seq), n)] or [[]]


# ===========================================================================
# Blog: news / recruitment / HR notices / factory list
# ===========================================================================
BLOG = DATA["blog"]
BLOG_CATS = [("tin-tuc", "Tin tức", "/tin-tuc/"), ("tuyen-dung", "Tuyển dụng", "/tuyen-dung/"),
             ("thong-bao-nhan-su", "Thông báo Nhân Sự", "/tin-tuc/thong-bao-nhan-su/"),
             ("danh-sach-nha-may", "Danh sách nhà máy", "/danh-sach-nha-may/")]
BLOG_CRUMBS = {"tin-tuc": [("Trang chủ", "/"), ("Tin tức", None)],
               "tuyen-dung": [("Trang chủ", "/"), ("Tuyển dụng", None)],
               "thong-bao-nhan-su": [("Trang chủ", "/"), ("Tin tức", "/tin-tuc/"), ("Thông báo Nhân Sự", None)],
               "danh-sach-nha-may": [("Trang chủ", "/"), ("Danh sách nhà máy", None)]}


def blog_side_cats(current):
    rows = []
    for key, name, path in BLOG_CATS:
        cls = ' class="current"' if key == current else ""
        rows.append(f'<div class="cate_item">{CHEVRON}<a{cls} href="{path}">{e(name)}</a></div>')
    return f'<div class="side-box"><div class="title_duanmoinhat">Chuyên mục</div><div class="box_duan_moinhat">{"".join(rows)}</div></div>'


def blog_side_popular():
    rows = []
    for p in BLOG["popular"]:
        rows.append(f'''<div class="box_sidebar_blog">
  <a class="img-inner" href="{norm(p["url"])}"><img src="{img(p["thumb"])}" alt="" loading="lazy"></a>
  <div class="sb-text"><a href="{norm(p["url"])}"><h4>{e(p["title"])}</h4></a>{date_html(p["date"])}</div>
</div>''')
    return f'<div class="side-box"><div class="title_duanmoinhat">Tin tức xem nhiều</div><div class="box_duan_moinhat">{"".join(rows)}</div></div>'


def blog_sidebar(current):
    return f'<aside class="blog-side">{blog_side_cats(current)}{blog_side_popular()}</aside>'


def blog_card(c):
    u = norm(c["url"])
    return f'''<div class="post-item"><div class="box-blog-post">
  <div class="box-image"><a class="image-cover" href="{u}" aria-label="{e(c["title"])}"><img src="{img(c["thumb"])}" alt="" loading="lazy"></a></div>
  <div class="box-text">
    <h5 class="post-title"><a href="{u}">{e(c["title"])}</a></h5>
    {date_html(c["date"])}
    <p class="from_the_blog_excerpt">{e(c["excerpt"])}</p>
    <a href="{u}" class="doc-tiep-tintuc">Đọc tiếp</a>
  </div>
</div></div>'''


def blog_archives():
    pages = []
    for key, name, path in BLOG_CATS:
        urls = BLOG["cats"][key]["posts"]
        groups = chunks(urls, PER_PAGE)
        for n, group in enumerate(groups, 1):
            cards = "".join(blog_card(BLOG["posts"][u]["card"]) for u in group)
            main = f'''<div class="page-title-cate">
  <div class="container"><h1 class="entry-title">{e(name)}</h1>{crumbs(BLOG_CRUMBS[key])}</div>
</div>
<section class="blog-section">
  <div class="container">
  <div class="blog-cats-mobile">{blog_side_cats(key)}</div>
  <div class="blog-row">
    {blog_sidebar(key)}
    <div class="blog-main">{cards}{pagination(path, n, len(groups), mid=3)}</div>
  </div></div>
</section>'''
            title = name if n == 1 else f"{name} - Trang {n} trên {len(groups)}"
            pages.append(Page(page_url(path, n), f"{title} - Thép minh cường", "page-blog", "Tin tức", main))
    return pages


def fix_post_content(content, post_path):
    """gallery thumbnails link to WordPress attachment pages -> open the image itself"""
    def repl(m):
        a_open, inner = m.group(1), m.group(2)
        src = re.search(r'src="([^"]+)"', inner)
        if not src:
            return m.group(0)
        return f'<a href="{img(src.group(1))}" data-lightbox="post">{inner}</a>'
    content = re.sub(r'(<a href="[^"]*(?:#main|/attachment/)[^"]*">)\s*(<img[^>]*>)\s*</a>', repl, content)
    content = re.sub(r'src="([^"]+)"', lambda m: f'src="{img(m.group(1))}" loading="lazy"', content)
    return content


def related_card(r):
    u = norm(r["url"])
    return f'''<div class="rel-col">
  <a class="img_inner" href="{u}"><img src="{img(r["thumb"])}" alt="" loading="lazy"></a>
  <a class="tit_lienquan" href="{u}"><h4>{e(r["title"])}</h4></a>
  {date_html(r["date"])}
  <div class="mota">{e(r["excerpt"])}</div>
</div>'''


def blog_posts():
    pages = []
    for url, p in BLOG["posts"].items():
        path = norm(url)
        crumb = [(t, norm(h) if h else None) for t, h in p["crumb"]]
        side_key = p["cats"][0] if p["cats"] else "tin-tuc"
        if side_key == "thong-bao-nhan-su":
            side_key = "tin-tuc"
        main = f'''<div class="blog_chitiet">
  <div class="breadcrumbs_duan">{crumbs(crumb + [], "breadcrumb")}</div>
  <section class="blog-section single">
    <div class="container">
    <div class="blog-cats-mobile">{blog_side_cats(side_key)}</div>
    <div class="blog-row">
      {blog_sidebar(side_key)}
      <div class="blog-main">
        <div class="tieu_de"><h1>{e(p["title"])}</h1>{date_html(p["date"])}</div>
        <div class="noidung_blog">{fix_post_content(p["content"], path)}</div>
      </div>
    </div>
    <div class="sharer-fb-du-an">{SHARE_FB.format(u=SITE + path)}</div>
    </div>
  </section>
  <section class="blog_lienquan">
    <div class="container">
      <div class="title"><h2>Tin tức liên quan</h2></div>
      <div class="list_blog_lienquan">{"".join(related_card(r) for r in p["related"])}</div>
    </div>
  </section>
</div>'''
        pages.append(Page(path, f"{p['title']} - Thép minh cường", "page-blog-single", "Tin tức", main))
    return pages


# ===========================================================================
# Projects (du-an)
# ===========================================================================
PROJ = DATA["projects"]
PROJ_CATS = {"du-an-nuoc-ngoai": ("Dự án Nước ngoài", "/du-an/du-an-nuoc-ngoai/"),
             "du-an-trong-nuoc": ("Dự án Trong nước", "/du-an/du-an-trong-nuoc/")}
ICONS_DA = ["/images/theme/icon-da-1.png", "/images/theme/icon-da-2.png", "/images/theme/icon-da-3.png"]


def all_projects():
    order = list(PROJ["cats"]["all"]["posts"])
    for key in PROJ_CATS:
        for u in PROJ["cats"][key]["posts"]:
            if u not in order:
                order.append(u)
    return order


def project_type(url):
    for key, (name, _) in PROJ_CATS.items():
        if url in PROJ["cats"][key]["posts"]:
            return key, name
    return "", ""


def project_search(type_label="Loại dự án"):
    opts = "".join(f'<option value="{k}">{e(n)}</option>' for k, (n, _) in PROJ_CATS.items())
    return f'''<section class="pj-search">
  <div class="container">
    <form class="handle_search_duan" action="/du-an/" method="get" role="search">
      <div class="col_search col_label"><h3>Tìm dự án</h3></div>
      <div class="col_search col_fields">
        <div class="inner_search"><input class="search_handle_duan" name="key" placeholder="Tìm dự án theo từ khóa" autocomplete="off"></div>
        <div class="inner_search_more loai_congtrinh"><select class="search_loaicongtrinh" name="loai-cong-trinh"><option value="">{e(type_label)}</option>{opts}</select></div>
      </div>
      <div class="col_search col_btn"><button class="button pj-search-btn" type="submit"><span>Tìm kiếm</span></button></div>
    </form>
  </div>
</section>'''


def project_card(url):
    p = PROJ["projects"][url]
    c = p["card"]
    imgs = c["images"] or p["gallery"]
    slides = "".join(f'<div class="pj-slide"><img src="{img(u)}" alt="" loading="lazy"></div>' for u in imgs)
    rows = []
    for i, (label, val) in enumerate(c["info"][:3]):
        rows.append(f'<div class="box_sec_congtrinh"><div class="icon"><img src="{ICONS_DA[i]}" alt="" width="35" height="35"></div>'
                    f'<div class="desc">{e(label)} <strong>{e(val)}</strong></div></div>')
    u = norm(url)
    return f'''<div class="box_duan">
  <div class="pj-col pj-col-media">
    <div class="pj-slider" data-pj-slider>
      <div class="pj-main"><div class="pj-track">{slides}</div></div>
      <div class="pj-thumbs"><div class="pj-ttrack">{slides}</div></div>
      <ul class="pj-dots"></ul>
    </div>
  </div>
  <div class="pj-col pj-col-info">
    <a href="{u}"><h3>{e(c["title"] or p["title"])}</h3></a>
    <div class="loai_congtrinh">{"".join(rows)}</div>
  </div>
</div>'''


def project_sidebar():
    cats = "".join(f'<div class="cate_item">{CHEVRON}<a href="{path}">{e(n)}</a></div>' for n, path in PROJ_CATS.values())
    latest = "".join(f'''<div class="col_duan_moi"><a href="{norm(x["url"])}">
  <div class="box_img"><img src="{img(x["thumb"])}" alt="" loading="lazy"></div><h3>{e(x["title"])}</h3></a></div>''' for x in PROJ["latest"])
    return f'''<aside class="pj-side">
  <div class="side-box"><div class="title_duanmoinhat">Chuyên mục</div><div class="box_duan_moinhat">{cats}</div></div>
  <div class="side-box"><div class="title_duanmoinhat">Dự án mới nhất</div><div class="box_duan_moinhat">{latest}</div></div>
</aside>'''


def project_hero(title, crumb, compact):
    cls = "pj-hero compact" if compact else "pj-hero"
    return f'''<div class="{cls}">
  <div class="pj-hero-bg" style="background-image:url(/images/theme/bg-cate-duan.jpg)"></div>
  <div class="container"><h1 class="entry-title">{e(title)}</h1>{crumbs(crumb)}</div>
</div>'''


def project_archives():
    pages = []
    lists = [("all", "/du-an/", all_projects(), "Khám phá các dự án đã thực hiện của Minh Cường",
              [("Trang chủ", "/"), ("Dự án", None)], False, "Loại dự án")]
    for key, (name, path) in PROJ_CATS.items():
        lists.append((key, path, PROJ["cats"][key]["posts"], name,
                      [("Trang chủ", "/"), ("Chuyên mục dự án", None), (name, None)], True, "Loại dịch vụ dự án"))
    for key, base, urls, title, crumb, compact, type_label in lists:
        groups = chunks(urls, PER_PAGE)
        for n, group in enumerate(groups, 1):
            cards = "".join(project_card(u) for u in group)
            main = f'''{project_hero(title, crumb, compact)}
{project_search(type_label)}
<section class="sec_duan_all">
  <div class="container"><div class="pj-row">
    {project_sidebar()}
    <div class="pj-list" data-pj-list>{cards}{pagination(base, n, len(groups))}</div>
  </div></div>
</section>'''
            name = "Dự án" if key == "all" else PROJ_CATS[key][0]
            pages.append(Page(page_url(base, n), f"{name} - Thép minh cường", "page-projects", "Dự án", main))
    return pages


INFO_ICON = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M5 4h14a1 1 0 011 1v14a1 1 0 01-1 1H5a1 1 0 01-1-1V5a1 1 0 011-1zm1 2v8.6l3.3-3.3a1 1 0 011.4 0L15 15.6l1.3-1.3a1 1 0 011.4 0l.3.3V6H6zm9 2.5a1.5 1.5 0 110 3 1.5 1.5 0 010-3z" fill="currentColor"/></svg>'


def project_details():
    pages = []
    for url, p in PROJ["projects"].items():
        path = norm(url)
        gallery = "".join(f'<a class="img_duan_thumb_detail" href="{img(g)}" data-lightbox="project"><img src="{img(g)}" alt="" loading="lazy"></a>' for g in p["gallery"])
        infos = []
        for i, (label, val, _icon) in enumerate(p["infos"][:3]):
            infos.append(f'''<div class="pj-info"><div class="pj-info-inner">
  <img src="{ICONS_DA[i]}" alt="" width="63" height="63">
  <div class="sub_icon"><div>{e(label)}</div>{f"<strong>{e(val)}</strong>" if val else ""}</div>
</div></div>''')
        others = "".join(project_card(o) for o in p["others"] if o in PROJ["projects"])
        main = f'''<div class="breadcrumbs_duan">{crumbs([("Trang chủ", "/"), ("Dự án", "/du-an/")])}</div>
{project_search()}
<section class="sec_detail_duan">
  <div class="container">
    <h1>{e(p["title"])}</h1>
    <div class="thu_vien_anh">
      <div class="thu_vien_inner">{gallery}</div>
      {f'<div class="total_thuvien"><img src="/images/theme/icon-gallery.png" alt="" width="16" height="16"><span>{len(p["gallery"]) - 1}</span></div>' if len(p["gallery"]) > 4 else ""}
    </div>
    <div class="sharer-fb-du-an">{SHARE_FB.format(u=SITE + path)}</div>
  </div>
</section>
<section class="sec_thongtin_congtrinh">
  <div class="container">
    <div class="tit"><h3>Thông tin dự án</h3></div>
    <div class="row_icon_congtrinh_2">{"".join(infos)}</div>
  </div>
</section>
<section class="sec_noidung_duan">
  <div class="container"><h3 class="tit"><strong>Mô tả về dự án</strong></h3><div class="text">{fix_post_content(p["desc_html"], path)}</div></div>
</section>
<section class="sec_thongtin_congtrinh pj-others">
  <div class="container">
    <div class="title-key"><h3>Dự án khác</h3></div>
    <div class="relatedcat">{others}</div>
  </div>
</section>'''
        pages.append(Page(path, f"{p['title']} - Thép minh cường", "page-project-single", "Dự án", main))
    return pages


def project_index():
    """search index used by /du-an/?key=... (client-side filtering)"""
    out = []
    for u in all_projects():
        key, _ = project_type(u)
        out.append({"t": PROJ["projects"][u]["card"]["title"] or PROJ["projects"][u]["title"], "k": key, "h": project_card(u)})
    return out


# ===========================================================================
# Services (dich-vu)
# ===========================================================================
SERV = DATA["services"]
SEEMORE = "Xem chi tiết"


def service_card(item, show_cate=True, cols="ser-col"):
    c = item
    u = norm(c["url"])
    cate = ""
    if show_cate and c.get("cate"):
        cate = f'<a class="ser-box--cate" href="{norm(c["cate"][1])}"><img src="/images/theme/cate-icon.svg" alt="" width="16" height="16"><span>{e(c["cate"][0])}</span></a>'
    return f'''<div class="{cols}"><div class="ser-box">
  <a class="ser-image image-zoom" href="{u}" title="{e(c["title"])}"><img src="{img(c["thumb"])}" alt="{e(c["title"])}" loading="lazy"></a>
  <div class="ser-text">
    <h3><a href="{u}">{e(c["title"])}</a></h3>
    {cate}
    {f"<p>{e(c['excerpt'])}</p>" if c.get("excerpt") else ""}
    <a class="ser-box--seemore" href="{u}">{SEEMORE}</a>
  </div>
</div></div>'''


def service_pages():
    pages = []
    # root: the 7 categories
    cats = "".join(f'''<div class="ser-col"><div class="ser-box">
  <a class="ser-image image-zoom" href="{c["path"]}" title="{e(c["name"])}"><img src="{img(c["thumb"])}" alt="{e(c["name"])}" loading="lazy"></a>
  <div class="ser-text"><h3><a href="{c["path"]}">{e(c["name"])}</a></h3></div>
</div></div>''' for c in SERV["root"])
    main = f'''<div id="main-dich-vu">
  <section class="title-dich-vu"><div class="container"><h1 class="page-title">Dịch vụ</h1></div></section>
  <section><div class="container"><div class="row-40">{cats}</div></div></section>
</div>'''
    pages.append(Page("/dich-vu/", "Dịch vụ - Thép minh cường", "page-services", "Sản phẩm &amp; Dịch vụ", main))
    # categories
    for path, c in SERV["cats"].items():
        groups = chunks(c["posts"], PER_PAGE)
        for n, group in enumerate(groups, 1):
            cards = "".join(service_card(SERV["items"][u]["card"]) for u in group)
            main = f'''<div id="main-dich-vu" class="ser-cat">
  <section class="title-dich-vu"><div class="container"><h1 class="page-title">{e(c["name"])}</h1></div></section>
  <section><div class="container"><div class="row-40">{cards}</div>{pagination(path, n, len(groups), cls="nav-pagination phan-trang")}</div></section>
</div>'''
            pages.append(Page(page_url(path, n), f"{c['name']} - Thép minh cường", "page-services", "Sản phẩm &amp; Dịch vụ", main))
    # single items
    for url, s in SERV["items"].items():
        path = norm(url)
        others = "".join(service_card(SERV["items"][o]["card"], show_cate=False) for o in s["others"] if o in SERV["items"])
        main = f'''<section id="single-dich-vu">
  <div class="container">
    {f'<div class="single-dich-vu--img"><img src="{img(s["image"])}" alt="{e(s["title"])}"></div>' if s["image"] else ""}
    <h1 class="single-dich-vu__title"><span>{e(s["title"])}</span></h1>
    <div class="single-dich-vu--content">{fix_post_content(s["content"], path)}</div>
  </div>
</section>
<section class="dich-vu-lienquan">
  <div class="container">
    <div class="title"><h2>Dịch vụ khác</h2></div>
    <div class="row-40">{others}</div>
  </div>
</section>'''
        pages.append(Page(path, f"{s['title']} - Thép minh cường", "page-service-single", "Sản phẩm &amp; Dịch vụ", main))
    return pages


# ===========================================================================
# Static pages
# ===========================================================================
MAP_HQ = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3721.6076968524267!2d105.84150497508367!3d21.12820098054613!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x313501072fcc2ffb%3A0x6eb3f3dfa316d649!2zTWluaCBDxrDhu51uZyBTdGVlbA!5e0!3m2!1svi!2s!4v1699005003566!5m2!1svi!2s"
FACTORIES = [
    ("Trụ sở chính", "Km 10, Quốc lộ 3, Cầu Đôi, Xã Đông Anh, TP.Hà Nội", "093.607.8586", "Thứ 2 - Thứ 7", MAP_HQ, ""),
    ("Nhà máy số 5", "KCN Ô tô 1-5, Xã Thư Lâm, TP.Hà Nội", "0906 242 315", "Thứ 2 - Thứ 6",
     "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3720.3755452303067!2d105.85078737508509!3d21.17723538050946!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x313501426fb4aedf%3A0x78e0725453588967!2zTmjDoCBNw6F5IDUgQ3R5IENQIENLIFhMIFRNIE1JTkggQ8avxqBORw!5e0!3m2!1svi!2s!4v1698746737008!5m2!1svi!2s", "ha-noi"),
    ("Nhà máy số 3", "Bãi Kính, Xã Thư Lâm, TP.Hà Nội", "0906242315", "Thứ 2 - Thứ 6",
     "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3720.848267032288!2d105.84948927508457!3d21.158435880523612!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31350117fb953bf3%3A0xc9271492c7f3608!2zTmjDoCBNw6F5IDNBIEN0eSBDUCBDSyBYTCBUTSBNSU5IIEPGr-G7nE5H!5e0!3m2!1svi!2s!4v1698746652006!5m2!1svi!2s", "ha-noi"),
    ("Nhà máy số 2", "Bãi Đá, Xã Thư Lâm, TP.Hà Nội", "024.3883.5397", "Thứ 2 - Thứ 7",
     "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3721.035431986622!2d105.85484267508433!3d21.150988180529094!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31350121424d62a9%3A0x7c01c29910b3ebed!2zTmjDoCBNw6F5IDIgQ3R5IENQIENLIFhMIFRNIE1JTkggQ8av4bucTkc!5e0!3m2!1svi!2s!4v1698746540597!5m2!1svi!2s", "ha-noi"),
    ("Nhà máy số 6", "KCN Nguyên Khê, Xã Phúc Thịnh, TP.Hà Nội", "024.3883.5397", "Thứ 2 - Thứ 6",
     "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d59542.785373868915!2d105.8097401!3d21.1355148!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x313501e4f809abf3%3A0xe50be2c6f8304d77!2zTmjDoCBtw6F5IDYgLSBjw7RuZyB0eSBDUCBDSyBYTCBUTSBNaW5oIEPGsOG7nW5n!5e0!3m2!1svi!2s!4v1758591016884!5m2!1svi!2s", "ha-noi"),
]
# province filter of the original (its AJAX returns the Hà Nội factories ordered 2, 3, 5, 6; other provinces are empty)
PROVINCES = [("ha-noi", "Hà nội", ["Nhà máy số 2", "Nhà máy số 3", "Nhà máy số 5", "Nhà máy số 6"]),
             ("hoa-binh", "Hòa bình", []), ("ninh-binh", "Ninh bình", []), ("ho-chi-minh", "Hồ chí minh", [])]
PIN = '<svg class="ic-pin" viewBox="3 1 18 22" width="13" height="18" aria-hidden="true"><path d="M18.36 16.36L12 22.73l-6.36-6.37a9 9 0 1112.72 0zM12 13a2 2 0 100-4 2 2 0 000 4z" fill="currentColor"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M21 16.42v3.54a1 1 0 01-.93 1A16 16 0 013 4.93 1 1 0 014 4h3.54a.5.5 0 01.5.45c.02.23.04.46.08.68a11 11 0 00.92 3.07.5.5 0 01-.16.62l-2.16 1.54a13 13 0 006.95 6.95l1.54-2.16a.5.5 0 01.62-.16 11 11 0 003.07.92c.22.04.45.06.68.08a.5.5 0 01.45.5z" fill="currentColor"/></svg>'
CLOCK = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M12 22a10 10 0 110-20 10 10 0 010 20zm1-10V7h-2v7h6v-2h-4z" fill="currentColor"/></svg>'


def factory_items(names):
    by_name = {f[0]: f for f in FACTORIES}
    items, maps = [], []
    for i, n in enumerate(names):
        name, addr, phone, days, src, _ = by_name[n]
        act = " active" if i == 0 else ""
        items.append(f'''<div class="vmap-item{act}" data-map="{i}">
  <h3>{e(name)}</h3>
  <div class="vmap-row">{PIN}<p>{e(addr)}</p></div>
  <div class="vmap-more">
    <a class="vmap-row" href="tel:{phone.replace(' ', '')}">{PHONE}<p>{e(phone)}</p></a>
    <div class="vmap-row">{CLOCK}<div><p><span>{e(days)}</span><span>(7H30 - 17H)</span></p></div></div>
  </div>
  <button class="vmap-toggle" type="button"></button>
</div>''')
        maps.append(f'<div class="vmap-map{act}" data-map="{i}"><iframe {"src" if i == 0 else "data-src"}="{src}" title="{e(name)}" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"></iframe></div>')
    return "".join(items), "".join(maps)


def factories_page():
    items, maps = factory_items([f[0] for f in FACTORIES])
    groups = {key: factory_items(names) for key, _, names in PROVINCES}
    tpl = "".join(f'<template data-province="{k}"><div class="vmap-list">{a}</div><div class="vmap-maps">{b}</div></template>' for k, (a, b) in groups.items())
    opts = "".join(f'<option value="{k}">{e(n)}</option>' for k, n, _ in PROVINCES)
    main = f'''<section class="banner-htch" style="background-image:url(/images/factories/bg-factories.jpg)">
  <div class="container"><h3>Hệ thống nhà máy</h3></div>
</section>
<section class="factories-ss">
  <div class="container">
    <div class="map-tong">
      <div class="vmap-left">
        <div class="vmap-left--header"><select class="vmap-select" aria-label="Danh sách nhà máy"><option value="">Danh sách nhà máy</option>{opts}</select></div>
        <div class="vmap-left--main"><div class="vmap-list">{items}</div></div>
      </div>
      <div class="vmap-right"><div class="vmap-maps">{maps}</div></div>
      {tpl}
    </div>
  </div>
</section>'''
    return [Page("/he-thong-nha-may/", "Hệ thống nhà máy - Thép minh cường", "page-factories", "", main)]


def contact_page():
    info = [("map-pin.png", "Địa chỉ", "<p>Km10, QL3, Cầu Đôi, Xã Đông Anh, Tp. Hà Nội</p>"),
            ("time.png", "Mở cửa", "<p>Thứ 2 đến thứ 7: 7h30 – 17h</p>"),
            ("mail.png", "E-mail", '<p><a href="mailto:contact@minhcuongsteel.com">contact@minhcuongsteel.com</a></p>'),
            ("phone.png", "Hotline", '<p><a href="tel:0936078586">093.607.8586</a></p><h3>TUYỂN DỤNG</h3><p><a href="tel:0913234986">0962.953.353&nbsp;</a></p>')]
    cells = "".join(f'<div class="ct-item"><img src="/images/contact/{i}" alt="" width="32" height="32"><h3>{t}</h3>{b}</div>' for i, t, b in info)
    main = f'''<section class="ct-hero" style="background-image:url(/images/contact/bg-contact-hero.jpg)">
  <div class="ct-hero-overlay"></div>
  <div class="container"><h1>Liên hệ</h1><p class="lead">Gửi tin nhắn cho chúng tôi</p></div>
</section>
<div class="ct-card-wrap">
  <div class="ct-card">
    <div class="ct-col">
      <h2>Liên hệ với chúng tôi</h2>
      <div class="ct-grid">{cells}</div>
    </div>
    <div class="ct-col">
      <h2>Đăng ký để nhận tư vấn</h2>
      <form class="contact-form ct-form" novalidate>
        <input type="text" name="name" placeholder="Họ tên" required>
        <input type="email" name="email" placeholder="Email">
        <input type="tel" name="phone" placeholder="Số điện thoại" required>
        <textarea name="note" rows="4" placeholder="Lời nhắn"></textarea>
        <input type="submit" value="Gửi thông tin">
        <div class="form-response" role="status"></div>
      </form>
    </div>
  </div>
</div>
<div class="ct-map"><iframe src="{MAP_HQ}" title="Bản đồ Minh Cường Steel" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"></iframe></div>'''
    return [Page("/lien-he/", "Liên hệ - Thép minh cường", "page-contact", "Liên hệ", main)]


def directions_page():
    main = '''<section class="plain-page">
  <div class="container">
    <div class="widget">
      <h4 class="widget-title">CTY CP CƠ KHÍ XÂY LẮP THƯƠNG MẠI MINH CƯỜNG</h4>
      <p><b>Địa chỉ:</b> Km10, QL3, Cầu Đôi, Uy Nỗ, Đông Anh, Hà Nội<br><b>Điện thoại:</b> 04.3883.5397 / Fax:3883.2305<br><b>VPĐD:</b> Tầng 4, Tháp A, tòa nhà sông Đà, đường Phạm Hùng, phường Mỹ Đình I, quận Nam Từ Liêm, Hà Nội</p>
    </div>
    <div class="widget">
      <h4 class="widget-title">ĐỊA CHỈ NHÀ MÁY</h4>
      <p><b>Nhà máy số 2:</b> Ấp Tó, Uy Nỗ, Đông Anh, Hà Nội<br><b>Điện thoại / Fax:</b> 043.883 8289<br><b>Nhà máy số 3:</b> Bãi Kính, Uy Nỗ, Đông Anh, Hà Nội<br><b>Điện thoại:</b> 0989.654.581 / Fax:043.9687022</p>
    </div>
  </div>
</section>'''
    return [Page("/ban-duong-di/", "Bản đồ đường đi - Thép minh cường", "page-plain", "", main)]


def build_pages():
    return (blog_archives() + blog_posts() + project_archives() + project_details()
            + service_pages() + factories_page() + contact_page() + directions_page())
