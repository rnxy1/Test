"""Zoom helper for readers: python3 crop.py <page.jpg> <x0> <y0> <x1> <y1> <out.jpg> [rotate_deg]
(fractions 0-1 of the page as stored; optional rotate_deg 90/180/270 counter-clockwise, applied to the crop)."""
import sys
from PIL import Image
src, x0, y0, x1, y1, out = sys.argv[1], *map(float, sys.argv[2:6]), sys.argv[6]
im = Image.open(src); W, H = im.size
c = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
if len(sys.argv) > 7: c = c.rotate(float(sys.argv[7]), expand=True)
if max(c.size) < 1600:
    f = 1600 / max(c.size); c = c.resize((int(c.width * f), int(c.height * f)), Image.LANCZOS)
c.save(out, quality=92); print(out, c.size)
