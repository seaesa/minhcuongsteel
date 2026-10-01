"""Download every content image referenced in data/site.json and store an optimised
WebP copy (max 1000px wide) under images/site/<yyyy>/<mm>/<name>.webp.

The mapping original-URL -> local path is written to data/images.json and used by
build_html.py. Already converted files are skipped, so the script can be re-run.

usage: python3 scripts/download_site_images.py
"""
import io
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/120 Safari/537.36",
      "Referer": "https://minhcuongsteel.com/"}
MAX_W = 1000
QUALITY = 74


def collect(d):
    urls = set()

    def add(u):
        if u and "wp-content/uploads" in u:
            urls.add(u.split("?")[0])

    def from_html(h):
        for m in re.findall(r'src="([^"]+)"', h):
            add(m)
        for m in re.findall(r'href="([^"]+\.(?:jpe?g|png|webp|gif))"', h, re.I):
            add(m)

    b = d["blog"]
    for p in b["posts"].values():
        add(p["card"]["thumb"])
        add(p["og_image"])
        from_html(p["content"])
        for r in p["related"]:
            add(r["thumb"])
    for x in b["popular"]:
        add(x["thumb"])
    pr = d["projects"]
    for p in pr["projects"].values():
        for g in p["gallery"] + p["card"]["images"]:
            add(g)
        from_html(p["desc_html"])
    for x in pr["latest"]:
        add(x["thumb"])
    sv = d["services"]
    for p in sv["items"].values():
        add(p["image"])
        add(p["card"]["thumb"])
        from_html(p["content"])
    for c in sv["root"]:
        add(c["thumb"])
    return sorted(urls)


def local_path(url):
    m = re.search(r"/uploads/(\d{4})/(\d{2})/([^/]+)$", url)
    if m:
        y, mo, name = m.groups()
    else:
        y, mo, name = "misc", "00", url.rsplit("/", 1)[-1]
    stem = re.sub(r"\.[a-z0-9]+$", "", name, flags=re.I)
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem)
    return f"images/site/{y}/{mo}/{stem}.webp"


def one(url):
    rel = local_path(url)
    out = ROOT / rel
    if out.exists() and out.stat().st_size > 0:
        return url, rel, "skip"
    try:
        req = urllib.request.Request(urllib.parse.quote(url, safe=":/%"), headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        im = Image.open(io.BytesIO(data))
        im = ImageOps.exif_transpose(im)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if "transparency" in im.info else "RGB")
        if im.width > MAX_W:
            im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
        out.parent.mkdir(parents=True, exist_ok=True)
        im.save(out, "WEBP", quality=QUALITY, method=5)
        return url, rel, "ok"
    except Exception as e:  # noqa: BLE001
        return url, None, f"ERR {e}"


if __name__ == "__main__":
    import urllib.parse  # noqa: F401  (used in one())

    data = json.loads((ROOT / "data/site.json").read_text(encoding="utf-8"))
    urls = collect(data)
    mapping, errors = {}, []
    with ThreadPoolExecutor(8) as ex:
        for i, (url, rel, status) in enumerate(ex.map(one, urls), 1):
            if rel:
                mapping[url] = "/" + rel
            else:
                errors.append((url, status))
            if i % 50 == 0:
                print(i, "/", len(urls), flush=True)
    (ROOT / "data/images.json").write_text(json.dumps(mapping, indent=0, ensure_ascii=False), encoding="utf-8")
    print("done", len(mapping), "errors", len(errors))
    for e in errors:
        print("  ", e)
