"""Recolour the original orange (#FC7200 family) in theme images to the site's green primary.
PNG: hue-shift saturated orange pixels (keeps shading/alpha). SVG: replace hex fills.
usage: python3 scripts/recolor_theme.py file [file ...]"""
import colorsys
import re
import sys
from pathlib import Path

from PIL import Image

TARGET = (0x16, 0xA3, 0x4A)
TH, TS, TV = colorsys.rgb_to_hsv(*(c / 255 for c in TARGET))


def recolor_png(path):
    im = Image.open(path).convert("RGBA")
    px = im.load()
    n = 0
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if s > 0.25 and 0.0 <= h < 0.13 and v > 0.3:
                nr, ng, nb = colorsys.hsv_to_rgb(TH, min(1, TS * s), v * TV)
                px[x, y] = (round(nr * 255), round(ng * 255), round(nb * 255), a)
                n += 1
    im.save(path, optimize=True)
    return n


def recolor_svg(path):
    s = Path(path).read_text(encoding="utf-8")
    new = re.sub(r"#F[A-F0-9]7[0-9A-F]0[0-9A-F]|#FC7200|#FF7A00|#F47920", "#16A34A", s, flags=re.I)
    Path(path).write_text(new, encoding="utf-8")
    return s != new


for f in sys.argv[1:]:
    print(f, recolor_svg(f) if f.endswith(".svg") else recolor_png(f))
