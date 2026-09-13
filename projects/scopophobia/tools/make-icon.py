#!/usr/bin/env python3
"""
Draws the pack icon — the little picture Minecraft shows next to the pack in
its list.

    python3 tools/make-icon.py

It is drawn at 64x64 and then blown up with no smoothing at all, so every pixel
stays a hard square. That is what makes it look like it belongs in the game
rather than like a photograph someone shrank.

Three copies come out, because the two editions want different names in
different places:

    java/pack.png                       Java looks for exactly this name
    bedrock/scopophobia_bp/pack_icon.png    and Bedrock for this one
    bedrock/scopophobia_rp/pack_icon.png    in each half of the add-on
    art/icon.png                        and one for the website
"""

import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = 64

SKY_TOP = (19, 25, 33)
SKY_LOW = (32, 39, 33)
TREE = (13, 20, 18)
HEAD = (11, 11, 14)
BODY = (9, 9, 12)
DARK = (6, 6, 8)
GROUND = (16, 20, 16)
EDGE = (74, 96, 110)
MOUTH = (240, 236, 226)
RIM = (86, 46, 40)


def disc(d, cx, cy, r, colour):
    """A filled circle drawn a pixel at a time, so it comes out round rather
    than as a smooth shape that has been squashed down to this size."""
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + r * 0.6:
                d.point((x, y), fill=colour)


def draw():
    img = Image.new("RGB", (N, N), SKY_TOP)
    d = ImageDraw.Draw(img)

    for y in range(N):
        t = (y / N) ** 1.3
        d.line([(0, y), (N, y)],
               fill=tuple(int(SKY_TOP[i] + (SKY_LOW[i] - SKY_TOP[i]) * t) for i in range(3)))

    # spruce trees down both edges: darker than the sky, lighter than the
    # creature, so the creature still reads as the blackest thing in the picture
    for x0, w, top in ((0, 4, 4), (6, 3, 12), (56, 3, 9), (60, 4, 3)):
        d.rectangle([x0, top, x0 + w, N], fill=TREE)
        for k in range(6):
            y = top + 3 + k * 9
            if y < N:
                d.rectangle([max(0, x0 - 2), y, min(N - 1, x0 + w + 2), y + 3], fill=TREE)

    d.rectangle([0, 58, N, N], fill=GROUND)

    # ---- the creature ----
    for x0 in (17, 42):                                   # arms, then claws
        d.rectangle([x0, 29, x0 + 4, 53], fill=BODY)
        d.rectangle([x0 + 1, 53, x0 + 3, 62], fill=DARK)
    d.rectangle([27, 50, 29, 62], fill=BODY)              # legs
    d.rectangle([34, 50, 36, 62], fill=BODY)
    d.rectangle([24, 29, 39, 52], fill=BODY)              # body
    d.rectangle([29, 24, 34, 30], fill=BODY)              # neck
    d.rectangle([22, 5, 41, 24], fill=HEAD)               # head

    # one edge catches the light, which is what stops it being a black blob
    d.rectangle([17, 29, 17, 53], fill=EDGE)
    d.rectangle([24, 29, 24, 52], fill=EDGE)
    d.rectangle([22, 5, 22, 24], fill=EDGE)
    d.rectangle([22, 5, 41, 5], fill=(40, 54, 62))

    # the mouth, and nothing else on the face. No highlight inside it: a
    # highlight makes it an eye, and it is not an eye.
    disc(d, 32, 15, 7, RIM)
    disc(d, 32, 15, 6, MOUTH)

    return img


def save(img, rel, size):
    path = os.path.join(HERE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.resize((size, size), Image.NEAREST).save(path, "PNG", optimize=True)
    print("%-44s %d x %d  %5.1f KB" % (rel, size, size, os.path.getsize(path) / 1024))


icon = draw()
save(icon, "java/pack.png", 128)
save(icon, "bedrock/scopophobia_bp/pack_icon.png", 256)
save(icon, "bedrock/scopophobia_rp/pack_icon.png", 256)
save(icon, "art/icon.png", 256)
