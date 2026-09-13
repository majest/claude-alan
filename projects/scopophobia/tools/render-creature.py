#!/usr/bin/env python3
"""
Draws the creature from the model the game actually uses.

    python3 tools/render-creature.py

The picture-making model on the other machine could not do this one. Asked for
a head with no eyes it kept putting eyes on anyway, because nearly every face
it has ever seen has two of them. Telling a model *not* to draw something is
the thing it is worst at.

So this does it properly instead: it reads
bedrock/scopophobia_rp/models/entity/hunter.geo.json, the same file Minecraft
reads, turns every box into six flat faces, bends the arms and legs into a
pose, and draws them furthest-away-first. What comes out is the real creature
rather than an impression of it.
"""

import json, math, os, glob
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEO = os.path.join(HERE, "bedrock", "scopophobia_rp", "models", "entity", "hunter.geo.json")
OUT = os.path.join(HERE, "art")

W = H = 640
FOCAL = 620.0
LIGHT = (-0.45, 0.80, -0.40)

SKIN = (36, 36, 43)        # the creature, lit
SHADE = (13, 13, 17)       # the creature, unlit
RIM = (108, 142, 160)      # cold light down one edge
MOUTH = (232, 228, 216)

# ---------------------------------------------------------------------------
# a very small amount of 3D maths
# ---------------------------------------------------------------------------
def ident():
    return [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]

def mul(a, b):
    out = []
    for r in range(3):
        row = []
        for c in range(4):
            v = sum(a[r][k] * (b[k][c] if k < 3 else 0) for k in range(3))
            if c == 3:
                v += a[r][3]
            row.append(v)
        out.append(row)
    return out

def apply(m, p):
    return tuple(m[r][0] * p[0] + m[r][1] * p[1] + m[r][2] * p[2] + m[r][3] for r in range(3))

def translate(x, y, z):
    return [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z]]

def rot(axis, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    if axis == "x":
        return [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0]]
    if axis == "y":
        return [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0]]
    return [[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0]]

def bone_matrix(parent, pivot, rx, ry, rz):
    m = mul(parent, translate(*pivot))
    for axis, deg in (("z", rz), ("y", ry), ("x", rx)):
        if deg:
            m = mul(m, rot(axis, deg))
    return mul(m, translate(-pivot[0], -pivot[1], -pivot[2]))

# ---------------------------------------------------------------------------
# the model
# ---------------------------------------------------------------------------
def load_bones():
    data = json.load(open(GEO))
    geo = data["minecraft:geometry"][0]
    bones = {}
    order = []
    for b in geo["bones"]:
        bones[b["name"]] = b
        order.append(b["name"])
    return bones, order

FACES = [
    ((0, 1, 2, 3), (0, 0, -1)),     # front  (the face with the mouth on it)
    ((5, 4, 7, 6), (0, 0, 1)),      # back
    ((4, 0, 3, 7), (-1, 0, 0)),     # left
    ((1, 5, 6, 2), (1, 0, 0)),      # right
    ((4, 5, 1, 0), (0, 1, 0)),      # top
    ((3, 2, 6, 7), (0, -1, 0)),     # bottom
]

def cube_corners(origin, size):
    x, y, z = origin
    w, h, d = size
    return [
        (x,     y + h, z),     (x + w, y + h, z),
        (x + w, y,     z),     (x,     y,     z),
        (x,     y + h, z + d), (x + w, y + h, z + d),
        (x + w, y,     z + d), (x,     y,     z + d),
    ]

# ---------------------------------------------------------------------------
# camera
# ---------------------------------------------------------------------------
def make_camera(yaw, pitch, distance, height):
    yr, pr = math.radians(yaw), math.radians(pitch)

    def project(p):
        x, y, z = p[0], p[1] - height, p[2]
        cx = x * math.cos(yr) + z * math.sin(yr)
        cz = -x * math.sin(yr) + z * math.cos(yr)
        cy = y * math.cos(pr) - cz * math.sin(pr)
        cz = y * math.sin(pr) + cz * math.cos(pr)
        cz += distance
        if cz < 1:
            cz = 1
        return (W / 2 + FOCAL * cx / cz, H / 2 - FOCAL * cy / cz, cz)

    def turn_normal(n):
        x, y, z = n
        cx = x * math.cos(yr) + z * math.sin(yr)
        cz = -x * math.sin(yr) + z * math.cos(yr)
        cy = y * math.cos(pr) - cz * math.sin(pr)
        return (cx, cy, cz)

    return project, turn_normal

def shade(normal):
    d = sum(normal[i] * LIGHT[i] for i in range(3))
    d = max(0.0, d)
    return tuple(int(SHADE[i] + (SKIN[i] - SHADE[i]) * (0.32 + 0.68 * d)) for i in range(3))

# ---------------------------------------------------------------------------
# poses. each is {bone: (rx, ry, rz)}
# ---------------------------------------------------------------------------
POSES = {
    "stand": {
        "arm_left": (4, 0, 6), "arm_right": (-2, 0, -6),
        "claw_left": (9, 0, 5), "claw_right": (-6, 0, -7),
    },
    "walk": {
        "leg_left": (34, 0, 0), "leg_right": (-34, 0, 0),
        "arm_left": (-14, 0, 7), "arm_right": (14, 0, -7),
        "claw_left": (16, 0, 4), "claw_right": (-12, 0, -6),
        "body": (2, 0, 0),
    },
    "reach": {
        "arm_left": (-74, 0, 16), "arm_right": (-68, 0, -14),
        "claw_left": (-28, 0, 8), "claw_right": (-24, 0, -8),
        "leg_left": (12, 0, 0), "leg_right": (-9, 0, 0),
        "head": (-8, 0, 0),
    },
    "climb": {
        "arm_left": (-168, 0, 14), "arm_right": (-142, 0, -12),
        "claw_left": (44, 0, 8), "claw_right": (38, 0, -8),
        "leg_left": (74, 0, 5), "leg_right": (42, 0, -5),
        "body": (6, 0, 0), "head": (-34, 0, 0),
    },
}

SHOTS = [
    ("stand",  "stand",  18,  0, 92, 20),
    ("walk",   "walk",  -34,  4, 88, 19),
    ("reach",  "reach",  10, -8, 66, 22),
    ("climb",  "climb",  38,  6, 92, 20),
    ("side",   "stand",  90,  0, 92, 20),
]

def render(pose_name, yaw, pitch, distance, height, background=None):
    bones, order = load_bones()
    pose = POSES[pose_name]
    world = {}
    for name in order:
        b = bones[name]
        parent = world.get(b.get("parent"), ident())
        rx, ry, rz = pose.get(name, (0, 0, 0))
        world[name] = bone_matrix(parent, tuple(b["pivot"]), rx, ry, rz)

    project, turn_normal = make_camera(yaw, pitch, distance, height)

    quads = []
    for name in order:
        b = bones[name]
        m = world[name]
        for cube in b.get("cubes", []):
            corners = [apply(m, c) for c in cube_corners(cube["origin"], cube["size"])]
            for idx, normal in FACES:
                pts = [project(corners[i]) for i in idx]
                n = apply([[m[r][0], m[r][1], m[r][2], 0] for r in range(3)], normal)
                n = turn_normal(n)
                if n[2] > 0.02:             # facing away from us
                    continue
                depth = sum(p[2] for p in pts) / 4
                quads.append((depth, [(p[0], p[1]) for p in pts], shade(n), n))

    # the mouth, as a ring of points on the front of the head
    head = world["head"]
    ring = []
    for i in range(28):
        a = i / 28 * math.tau
        p = (math.cos(a) * 1.45, 30.2 + math.sin(a) * 1.45, -3.55)
        q = project(apply(head, p))
        ring.append((q[0], q[1]))
    mouth_depth = min(q[2] for q in
                      [project(apply(head, (0, 30.2, -3.6)))]) - 0.4

    # Draw onto nothing, so the figure can be cut out and placed afterwards.
    # Framing a 3D camera by hand is fiddly; cutting out what it drew and
    # putting it where you want it is not.
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    quads.append((mouth_depth, ring, MOUTH, None))
    for depth, pts, colour, normal in sorted(quads, key=lambda q: -q[0]):
        if colour is MOUTH:
            d.polygon(pts, fill=MOUTH + (255,))
            continue
        d.polygon(pts, fill=colour + (255,))
        if normal and normal[0] < -0.55:
            d.line(pts + [pts[0]], fill=RIM + (170,), width=2)

    return layer.crop(layer.getbbox())


# ---------------------------------------------------------------------------
# putting it in a picture
# ---------------------------------------------------------------------------
def backdrop(name, backdrops):
    """A plain dark room, or one of the pictures the other machine made."""
    if name and name in backdrops:
        img = backdrops[name].copy().resize((W, H))
        return Image.eval(img, lambda v: int(v * 0.5))
    img = Image.new("RGB", (W, H), (10, 12, 15))
    g = ImageDraw.Draw(img)
    horizon = int(H * 0.72)
    for y in range(H):
        if y < horizon:
            t = y / horizon
            g.line([(0, y), (W, y)], fill=(int(9 + 13 * t), int(11 + 15 * t), int(15 + 19 * t)))
        else:
            t = (y - horizon) / (H - horizon)
            g.line([(0, y), (W, y)], fill=(int(20 - 9 * t), int(22 - 10 * t), int(26 - 12 * t)))
    return img


def compose(cutout, back, feet_y, height_px, centre_x):
    """Stand the creature on the ground at a size we choose."""
    scale = height_px / cutout.height
    art = cutout.resize((max(1, int(cutout.width * scale)), height_px), Image.LANCZOS)
    x = int(centre_x - art.width / 2)
    y = int(feet_y - art.height)

    shadow = Image.new("RGBA", back.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    rx = int(art.width * 0.72)
    ry = max(4, int(art.width * 0.17))
    sd.ellipse([centre_x - rx, feet_y - ry, centre_x + rx, feet_y + ry], fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(rx * 0.24))

    out = Image.alpha_composite(back.convert("RGBA"), shadow)
    out.alpha_composite(art, (x, y))
    return out.convert("RGB")


def main():
    os.makedirs(OUT, exist_ok=True)
    backdrops = {}
    for name in ("giant-spruce", "bunker-room", "bunker-chests", "day-five",
                 "bunker-surface", "bunker-cave", "creature-climbing"):
        p = os.path.join(OUT, name + ".webp")
        if os.path.exists(p):
            backdrops[name] = Image.open(p).convert("RGB").filter(ImageFilter.GaussianBlur(1.2))

    # name,            pose,    yaw, pitch, backdrop,        feet,  height, x
    plan = [
        ("hunter-stand", "stand",  18,  0, None,            0.90, 0.74, 0.50),
        ("hunter-behind","walk",  148,  2, None,            0.90, 0.74, 0.50),
        ("hunter-walk",  "walk",  -34,  3, "giant-spruce",  0.94, 0.80, 0.44),
        ("hunter-reach", "reach",  10, -6, "bunker-room",   0.99, 0.92, 0.52),
        ("hunter-climb", "climb",  76,  2, "creature-climbing", 0.96, 0.86, 0.40),
        ("hunter-far",   "walk",   -8,  0, "bunker-surface",0.74, 0.30, 0.62),
        ("hunter-store", "reach",  62, -4, "bunker-chests", 0.97, 0.86, 0.34),
    ]
    for name, pose, yaw, pitch, bg, feet, tall, cx in plan:
        cutout = render(pose, yaw, pitch, 90, 20)
        img = compose(cutout, backdrop(bg, backdrops),
                      int(H * feet), int(H * tall), int(W * cx))
        path = os.path.join(OUT, name + ".webp")
        img.save(path, "WEBP", quality=86, method=6)
        print("%-22s %6.1f KB" % (name, os.path.getsize(path) / 1024))


if __name__ == "__main__":
    main()
