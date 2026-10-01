"""Scrape the content of minhcuongsteel.com (news, recruitment, projects, services)
into data/site.json so build_html.py can render every page locally.

HTML responses are cached in data/cache/ (delete it to re-fetch).
Images are NOT downloaded here: every image URL is recorded and fetched by
scripts/download_site_images.py.

usage: python3 scripts/scrape_site.py
"""
import hashlib
import json
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data/cache"
SITE = "https://minhcuongsteel.com"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/120 Safari/537.36"}

BLOG_CATS = [
    ("tin-tuc", "Tin tức", "/tin-tuc/"),
    ("tuyen-dung", "Tuyển dụng", "/tuyen-dung/"),
    ("thong-bao-nhan-su", "Thông báo Nhân Sự", "/tin-tuc/thong-bao-nhan-su/"),
    ("danh-sach-nha-may", "Danh sách nhà máy", "/danh-sach-nha-may/"),
]
PROJECT_CATS = [
    ("all", "Dự án", "/du-an/"),
    ("du-an-nuoc-ngoai", "Dự án Nước ngoài", "/du-an/du-an-nuoc-ngoai/"),
    ("du-an-trong-nuoc", "Dự án Trong nước", "/du-an/du-an-trong-nuoc/"),
]
SERVICE_CATS = [
    "/dich-vu/ket-cau-thep-ton-lop/", "/dich-vu/luoi-thep-han/", "/dich-vu/tu-van-thiet-ke/",
    "/dich-vu/kinh-doanh-thep/", "/dich-vu/long-thep-tru-hang/", "/dich-vu/dich-vu-cau-van-tai/",
    "/dich-vu/san-pham-khac/",
]


# ---------------------------------------------------------------------------
# fetching
# ---------------------------------------------------------------------------
def fetch(url):
    url = url if url.startswith("http") else SITE + url
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / (hashlib.md5(url.encode()).hexdigest() + ".html")
    if f.exists():
        return f.read_text(encoding="utf-8")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                html = r.read().decode("utf-8", "ignore")
            f.write_text(html, encoding="utf-8")
            return html
        except Exception as e:  # noqa: BLE001
            if getattr(e, "code", None) == 404:
                return ""
            time.sleep(2 + attempt * 3)
    raise RuntimeError("failed " + url)


def soup(url):
    return BeautifulSoup(fetch(url), "lxml")


def path_of(url):
    """absolute site URL -> site path ('/tin-tuc/'), other URLs unchanged"""
    if url and url.startswith(SITE):
        p = urlparse(url).path or "/"
        return p
    return url


def text(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip() if el else ""


def img_src(img):
    if img is None:
        return ""
    for a in ("data-lazy-src", "data-src", "src"):
        v = img.get(a)
        if v and not v.startswith("data:"):
            return v
    return ""


def best_src(img, max_w=1100):
    """pick the largest srcset candidate <= max_w (falls back to src)"""
    src = img_src(img)
    srcset = img.get("data-srcset") or img.get("data-lazy-srcset") or img.get("srcset") or ""
    best, best_w = None, 0
    for part in srcset.split(","):
        bits = part.strip().split()
        if len(bits) == 2 and bits[1].endswith("w"):
            w = int(bits[1][:-1])
            if best_w < w <= max_w:
                best, best_w = bits[0], w
    return best or src


def pages_of(s):
    nums = [int(n) for n in re.findall(r"/page/(\d+)/", str(s))]
    return max(nums) if nums else 1


def cf_decode(hexstr):
    key = int(hexstr[:2], 16)
    return "".join(chr(int(hexstr[i:i + 2], 16) ^ key) for i in range(2, len(hexstr), 2))


def clean_html(el):
    """content HTML: drop scripts/noscript, resolve lazy images, keep links/structure"""
    if el is None:
        return ""
    el = BeautifulSoup(str(el), "lxml").find(el.name)
    for t in el.select("script, style, noscript, .sharedaddy, iframe[src*='facebook.com/plugins']"):
        t.decompose()
    # Cloudflare email obfuscation -> plain mailto links / text
    for sp in el.select("[data-cfemail]"):
        sp.replace_with(cf_decode(sp["data-cfemail"]))
    for a in el.select('a[href*="/cdn-cgi/l/email-protection"]'):
        enc = a["href"].split("#", 1)[1] if "#" in a["href"] else ""
        a["href"] = "mailto:" + cf_decode(enc) if enc else "mailto:" + a.get_text(strip=True)
    for img in el.find_all("img"):
        src = best_src(img)
        attrs = {"src": src, "alt": img.get("alt", "")}
        if img.get("width") and img.get("height"):
            attrs["width"], attrs["height"] = img["width"], img["height"]
        img.attrs = attrs
    for a in el.find_all(True):
        for att in list(a.attrs):
            if att.startswith("data-") or att in ("srcset", "sizes", "decoding", "fetchpriority", "loading"):
                del a.attrs[att]
    for iframe in el.find_all("iframe"):
        if not iframe.get("src") and iframe.get("data-src"):
            iframe["src"] = iframe["data-src"]
    return "".join(str(c) for c in el.contents).strip()


# ---------------------------------------------------------------------------
# blog (news / recruitment / hr notices / factory list)
# ---------------------------------------------------------------------------
def parse_blog_archive_items(s):
    items = []
    for it in s.select("#col-484919012 .post-item"):
        a = it.select_one(".post-title a")
        img = it.select_one(".box-image img")
        items.append({
            "url": path_of(a["href"]),
            "title": text(a),
            "thumb": img_src(img),
            "date": text(it.select_one(".date_inner")),
            "excerpt": text(it.select_one(".from_the_blog_excerpt")),
        })
    return items


def parse_sidebar_popular(s):
    out = []
    for b in s.select(".chuyen_muc_maytinh .box_sidebar_blog"):
        a = b.select_one(".title a")
        out.append({"url": path_of(a["href"]), "title": text(b.select_one("h4")),
                    "thumb": best_src(b.select_one("img"), 400), "date": text(b.select_one(".date_inner"))})
    return out


def scrape_blog():
    cats, cards, popular = {}, {}, []
    for key, name, path in BLOG_CATS:
        first = soup(path)
        n = pages_of(first.select_one(".nav-pagination") or "")
        order = []
        for p in range(1, n + 1):
            s = first if p == 1 else soup(f"{path}page/{p}/")
            for item in parse_blog_archive_items(s):
                order.append(item["url"])
                cards.setdefault(item["url"], item)
            if not popular:
                popular = parse_sidebar_popular(s)
        cats[key] = {"name": name, "path": path, "posts": order}
        print(f"blog {key}: {len(order)} posts / {n} pages")

    def post(url):
        s = soup(url)
        body = s.select_one(".noidung_blog")
        crumbs = [a for a in s.select(".breadcrumbs_duan a")]
        related = []
        for c in s.select(".list_blog_lienquan > .col"):
            a = c.select_one("a.tit_lienquan")
            related.append({"url": path_of(a["href"]), "title": text(a), "thumb": best_src(c.select_one("img"), 700),
                            "date": text(c.select_one(".date_inner")), "excerpt": text(c.select_one(".mota"))})
        og = s.select_one('meta[property="og:image"]')
        return url, {
            "url": url,
            "title": text(s.select_one(".tieu_de h1")),
            "date": text(s.select_one(".tieu_de .date_inner")),
            "crumb": [(text(a), path_of(a["href"])) for a in crumbs],
            "content": clean_html(body),
            "related": related,
            "og_image": og["content"] if og else "",
            "description": (s.select_one('meta[name="description"]') or {}).get("content", ""),
        }

    with ThreadPoolExecutor(6) as ex:
        posts = dict(ex.map(post, list(cards)))
    for url, p in posts.items():
        p["card"] = cards[url]
        p["cats"] = [k for k, c in cats.items() if url in c["posts"]]
    return {"cats": cats, "posts": posts, "popular": popular}


# ---------------------------------------------------------------------------
# projects (du-an)
# ---------------------------------------------------------------------------
def parse_project_card(box):
    title_a = box.select_one("a[href] > h3")
    title_a = title_a.parent if title_a else None
    imgs = []
    for img in box.select(".slider_duan_1 img"):
        u = img_src(img)
        if u and u not in imgs:
            imgs.append(u)
    info = []
    for d in box.select(".box_sec_congtrinh .desc"):
        strong = d.select_one("strong")
        val = text(strong)
        label = text(d)[: len(text(d)) - len(val)].strip() if val else text(d)
        info.append([label, val])
    pid = ""
    sl = box.select_one(".slider_duan_1")
    if sl:
        m = re.search(r"slider_duan_(\d+)", " ".join(sl.get("class", [])))
        pid = m.group(1) if m else ""
    return {"url": path_of(title_a["href"]) if title_a else "", "title": text(title_a), "images": imgs, "info": info, "id": pid}


def scrape_projects():
    cats, cards = {}, {}
    latest = []
    for key, name, path in PROJECT_CATS:
        first = soup(path)
        n = pages_of(first.select_one(".sec_duan_all .nav-pagination, .sec_duan_all .phan-trang, .sec_duan_all") or "")
        order = []
        for p in range(1, n + 1):
            s = first if p == 1 else soup(f"{path}page/{p}/")
            col = s.select_one(".sec_duan_all .large-8") or s.select_one(".sec_duan_all")
            if col is None:  # the original's pagination links to pages that 404
                continue
            for box in col.select(".box_duan"):
                c = parse_project_card(box)
                if c["url"]:
                    order.append(c["url"])
                    cards.setdefault(c["url"], c)
            if not latest:
                for b in s.select(".col_duan_moinhat .col_duan_moi"):
                    a = b.select_one("a[href]")
                    latest.append({"url": path_of(a["href"]), "title": text(b.select_one("h3")),
                                   "thumb": best_src(b.select_one("img"), 700)})
        cats[key] = {"name": name, "path": path, "posts": order}
        print(f"projects {key}: {len(order)} / {n} pages")

    def detail(url):
        s = soup(url)
        gallery = [a.get("data-src") or img_src(a.select_one("img")) for a in s.select(".thu_vien_inner a.img_duan_thumb_detail")]
        infos = []
        for col in s.select(".row_icon_congtrinh_2 > .col"):
            sub = col.select_one(".sub_icon")
            label = text(sub.select_one("div")) if sub else ""
            infos.append([label, text(sub.select_one("strong")) if sub else "", img_src(col.select_one(".icon img"))])
        desc = s.select_one(".sec_noidung_duan .ban_viet")
        others = [parse_project_card(b)["url"] for b in s.select(".relatedcat .box_duan")]
        return url, {
            "url": url,
            "title": text(s.select_one(".sec_detail_duan h1")),
            "gallery": [g for g in gallery if g],
            "infos": infos,
            "desc_html": clean_html(desc),
            "others": [o for o in others if o],
        }

    with ThreadPoolExecutor(6) as ex:
        details = dict(ex.map(detail, list(cards)))
    for url, d in details.items():
        d["card"] = cards[url]
        d["cats"] = [k for k, c in cats.items() if url in c["posts"] and k != "all"]
    return {"cats": cats, "projects": details, "latest": latest}


# ---------------------------------------------------------------------------
# services (dich-vu)
# ---------------------------------------------------------------------------
def parse_service_cards(s, scope="#main-dich-vu"):
    out = []
    for box in s.select(scope + " .ser-box"):
        a = box.select_one("h3 a")
        cate = box.select_one(".ser-box--cate")
        out.append({
            "url": path_of(a["href"]),
            "title": text(a),
            "thumb": img_src(box.select_one(".box-image img")),
            "cate": [text(cate), path_of(cate["href"])] if cate else None,
            "excerpt": text(box.select_one(".box-text-inner > p")),
        })
    return out


def scrape_services():
    root = soup("/dich-vu/")
    cats = []
    for c in parse_service_cards(root, "#main-dich-vu"):
        cats.append({"path": c["url"], "name": c["title"], "thumb": c["thumb"]})
    items, cat_lists = {}, {}
    for path in SERVICE_CATS:
        first = soup(path)
        n = pages_of(first.select_one(".phan-trang") or "")
        order = []
        name = text(first.select_one(".title-dich-vu h1, h1"))
        for p in range(1, n + 1):
            s = first if p == 1 else soup(f"{path}page/{p}/")
            for c in parse_service_cards(s):
                order.append(c["url"])
                items.setdefault(c["url"], c)
        cat_lists[path] = {"name": name, "posts": order}
        print(f"services {path}: {len(order)} / {n} pages")

    def detail(url):
        s = soup(url)
        others = [c["url"] for c in parse_service_cards(s, ".dich-vu-lienquan")]
        return url, {
            "url": url,
            "title": text(s.select_one(".single-dich-vu__title")),
            "image": img_src(s.select_one(".single-dich-vu--img img")),
            "content": clean_html(s.select_one(".single-dich-vu--content")),
            "others": others,
        }

    with ThreadPoolExecutor(6) as ex:
        details = dict(ex.map(detail, list(items)))
    for url, d in details.items():
        d["card"] = items[url]
        d["cats"] = [p for p, c in cat_lists.items() if url in c["posts"]]
    return {"root": cats, "cats": cat_lists, "items": details}


if __name__ == "__main__":
    data = {"blog": scrape_blog(), "projects": scrape_projects(), "services": scrape_services()}
    out = ROOT / "data/site.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", out, out.stat().st_size)
