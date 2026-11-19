"""Draws the app icons at deploy time (GitHub Actions). Usage: python make_icons.py <output_dir>"""
import sys
from PIL import Image, ImageDraw, ImageFont

NAVY, RED, WHITE, DEEP = (0, 45, 108), (197, 18, 48), (255, 255, 255), (1, 27, 72)
FONTS = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]

def font(px):
    for f in FONTS:
        try:
            return ImageFont.truetype(f, px)
        except OSError:
            pass
    return ImageFont.load_default(size=px)

def icon(size):
    im = Image.new("RGB", (size, size), NAVY)
    d = ImageDraw.Draw(im)
    s = size / 512
    x0, y0, x1, y1 = 136 * s, 128 * s, 376 * s, 368 * s
    d.rounded_rectangle([x0, y0 + 14 * s, x1, y1 + 14 * s], radius=34 * s, fill=RED)
    d.rounded_rectangle([x0, y0, x1, y1], radius=34 * s, fill=DEEP, outline=WHITE, width=max(2, int(6 * s)))
    f = font(int(190 * s))
    bb = d.textbbox((0, 0), "?", font=f)
    tx = (size - (bb[2] - bb[0])) / 2 - bb[0]
    ty = (y0 + y1) / 2 - (bb[3] - bb[1]) / 2 - bb[1]
    d.text((tx + 9 * s, ty + 9 * s), "?", font=f, fill=RED)
    d.text((tx, ty), "?", font=f, fill=WHITE)
    return im

out = sys.argv[1] if len(sys.argv) > 1 else "."
for n in (192, 512):
    icon(n).save(f"{out}/icon-{n}.png", optimize=True)
