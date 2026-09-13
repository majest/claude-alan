#!/usr/bin/env python3
"""
Builds the generated parts of the Bedrock add-on: the bunker, the giant
spruce, and the creature's texture.

    python3 tools/make-bedrock.py

Bedrock is not Java with a different name on it. Three things had to change.

  * No ladders or doors are placed, and no block states are set anywhere.
    Bedrock writes block states differently from Java and gets them wrong
    quietly, so the way down is a spiral staircase made of plain blocks.
  * Chests are filled with replaceitem, which cannot set how worn out a tool
    is, so the iron down there is whole rather than nearly finished.
  * The book is not placed here. The script writes the words onto signs
    instead, because no Bedrock command can put text in a book.
"""
import os, random, zlib, struct

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BP = os.path.join(HERE, "bedrock", "scopophobia_bp")
RP = os.path.join(HERE, "bedrock", "scopophobia_rp")

BRICK = "minecraft:stone_bricks"
AIR = "minecraft:air"
FLOOR, CEIL = -22, -16
IN_LO, IN_HI = -21, -17
RC_X, RC_Z = -5, -5
R_IN, R_OUT = 10, 11

def rel(v):
    return "~" if v == 0 else "~%d" % v

def fill(x1, y1, z1, x2, y2, z2, block, mode=""):
    line = "fill %s %s %s %s %s %s %s" % (
        rel(x1), rel(y1), rel(z1), rel(x2), rel(y2), rel(z2), block)
    return line + (" " + mode if mode else "")

def setb(x, y, z, block):
    return "setblock %s %s %s %s" % (rel(x), rel(y), rel(z), block)

def disc_rows(cx, cz, r):
    rows = []
    for z in range(cz - r, cz + r + 1):
        dz = z - cz
        half = int((r * r - dz * dz) ** 0.5)
        rows.append((z, cx - half, cx + half))
    return rows

def cylinder(cx, cz, r, y1, y2, block):
    return [fill(x1, y1, z, x2, y2, z, block) for z, x1, x2 in disc_rows(cx, cz, r)]

def ellipsoid(cx, cy, cz, rx, ry, rz, block):
    out = []
    for y in range(cy - ry, cy + ry + 1):
        fy = 1 - ((y - cy) / ry) ** 2
        if fy <= 0:
            continue
        for z in range(cz - rz, cz + rz + 1):
            fz = fy - ((z - cz) / rz) ** 2
            if fz <= 0:
                continue
            half = int(rx * (fz ** 0.5))
            out.append(fill(cx - half, y, z, cx + half, y, z, block))
    return out

# --------------------------------------------------------------------------
# the spiral staircase: one step per block down, walking round a square ring
# --------------------------------------------------------------------------
RING = [(2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (-1, 2), (-2, 2), (-2, 1),
        (-2, 0), (-2, -1), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (2, -1)]

def stair_path(steps):
    path = [(0, 0), (1, 0)]
    i = 0
    while len(path) < steps:
        path.append(RING[i % len(RING)])
        i += 1
    return path[:steps]

def bunker():
    L = ["# built by tools/make-bedrock.py — do not edit by hand",
         "# the abandoned bunker: a circle on the surface, four rooms below"]

    L.append("# solid stone brick first, carved out afterwards")
    L += cylinder(RC_X, RC_Z, R_OUT, FLOOR, CEIL, BRICK)
    L.append(fill(-15, FLOOR, -35, 5, CEIL, -16, BRICK))
    L.append(fill(6, FLOOR, -13, 23, CEIL, 3, BRICK))
    L.append(fill(-9, FLOOR, 6, -1, CEIL, 17, BRICK))
    L.append(fill(-20, FLOOR, -8, -16, CEIL, -2, BRICK))

    L.append("# the round room, and the cylinder standing in the middle of it")
    L += cylinder(RC_X, RC_Z, R_IN, IN_LO, IN_HI, AIR)
    L += cylinder(RC_X, RC_Z, 3, IN_LO, IN_HI, BRICK)
    L += cylinder(RC_X, RC_Z, 3, IN_HI, IN_HI, "minecraft:chiseled_stone_bricks")
    L.append(fill(RC_X - 1, IN_LO + 1, RC_Z - 4, RC_X + 1, IN_LO + 1, RC_Z - 4, "minecraft:iron_block"))

    L.append("# north: the store room")
    L.append(fill(-5, IN_LO, -20, -5, IN_LO + 1, -16, AIR))
    L.append(fill(-14, IN_LO, -34, 4, IN_HI, -20, AIR))
    L.append("# east: collapsed")
    L.append(fill(6, IN_LO, -5, 9, IN_LO + 1, -5, AIR))
    L.append(fill(10, IN_LO, -12, 22, IN_HI, 2, AIR))
    L.append("# south: the small room")
    L.append(fill(-5, IN_LO, 6, -5, IN_LO + 1, 10, AIR))
    L.append(fill(-8, IN_LO, 11, -2, IN_HI, 16, AIR))
    L.append("# west: straight into a cave")
    L.append(fill(-19, IN_LO, -5, -16, IN_LO + 1, -5, AIR))
    L += ellipsoid(-34, -24, -5, 14, 9, 12, AIR)
    L.append(fill(-24, IN_LO, -5, -20, IN_LO + 1, -5, AIR))

    rng = random.Random(7)
    L.append("# rubble in the east room")
    for i in range(70):
        x, z, h = rng.randint(10, 22), rng.randint(-12, 2), rng.randint(1, 5)
        block = rng.choice(["minecraft:cobblestone", "minecraft:gravel", "minecraft:stone",
                            "minecraft:cracked_stone_bricks", "minecraft:andesite"])
        L.append(fill(x, IN_LO, z, x, IN_LO + h - 1, z, block))
    L.append(fill(13, IN_LO, -6, 19, IN_HI, 0, "minecraft:cobblestone"))
    L.append(fill(7, IN_LO, -5, 9, IN_LO + 1, -5, "minecraft:gravel"))

    L.append("# the stairwell, and a spiral staircase of plain blocks down it")
    L.append(fill(-2, -1, -2, 2, -17, 2, AIR))
    for i, (x, z) in enumerate(stair_path(21)):
        L.append(setb(x, -1 - i, z, BRICK))

    L.append("# the circle of stone bricks on the surface")
    L += cylinder(0, 0, 6, 0, 0, BRICK)
    L.append(fill(-7, 1, -7, 7, 4, 7, AIR))
    for z, x1, x2 in disc_rows(0, 0, 6):
        for x in (x1, x2):
            if abs(x) + abs(z) >= 6:
                L.append(setb(x, 1, z, "minecraft:iron_bars"))
    for x, z in [(0, -6), (0, 6), (-6, 0), (6, 0)]:
        L.append(setb(x, 1, z, "minecraft:iron_bars"))
    L.append(setb(0, 0, 0, "minecraft:iron_trapdoor"))

    L.append("# two rows of double chests in the north room")
    for row_z in (-25, -30):
        for x in (-11, -7, -3, 1):
            L.append(setb(x, IN_LO, row_z, "minecraft:chest"))
            L.append(setb(x + 1, IN_LO, row_z, "minecraft:chest"))
    L.append("# and the one chest in the small room to the south")
    L.append(setb(-5, IN_LO, 13, "minecraft:chest"))

    rng = random.Random(11)
    for i in range(16):
        L.append(setb(rng.randint(RC_X - 8, RC_X + 8), CEIL - 1,
                      rng.randint(RC_Z - 8, RC_Z + 8), "minecraft:soul_lantern"))
    for i in range(80):
        x, z = rng.randint(-16, 22), rng.randint(-34, 16)
        y = rng.choice([FLOOR, CEIL])
        L.append(setb(x, y, z, rng.choice(["minecraft:cracked_stone_bricks",
                                           "minecraft:mossy_stone_bricks"])))
    L.append("function bunker/loot")
    return L

FOOD = ["minecraft:cooked_beef", "minecraft:cooked_porkchop", "minecraft:bread",
        "minecraft:cooked_chicken", "minecraft:baked_potato", "minecraft:cooked_cod"]
GEAR = ["minecraft:iron_sword", "minecraft:iron_pickaxe", "minecraft:iron_axe",
        "minecraft:iron_shovel", "minecraft:iron_helmet", "minecraft:iron_chestplate",
        "minecraft:iron_leggings", "minecraft:iron_boots"]

def loot():
    rng = random.Random(23)
    L = ["# built by tools/make-bedrock.py — do not edit by hand",
         "# replaceitem cannot say how worn out a tool is, so on Bedrock the",
         "# iron down here is whole. On Java it is nearly finished."]
    for row_z in (-25, -30):
        for x in (-11, -7, -3, 1):
            for half in (0, 1):
                for slot in rng.sample(range(27), rng.randint(3, 7)):
                    roll = rng.random()
                    if roll < 0.45:
                        item, n = rng.choice(FOOD), rng.randint(1, 6)
                    elif roll < 0.8:
                        item, n = rng.choice(GEAR), 1
                    else:
                        item, n = "minecraft:cobblestone", rng.randint(8, 41)
                    L.append("replaceitem block %s %s %s slot.container %d %s %d" % (
                        rel(x + half), rel(IN_LO), rel(row_z), slot, item, n))
    L.append("replaceitem block %s %s %s slot.container 13 minecraft:writable_book 1"
             % (rel(-5), rel(IN_LO), rel(13)))
    return L

LOG = "minecraft:spruce_log"
LEAF = "minecraft:spruce_leaves"

def giant_spruce():
    H = 34
    L = ["# built by tools/make-bedrock.py — do not edit by hand", "# one giant spruce"]
    L.append(fill(0, 1, 0, 1, H, 1, LOG))
    L.append(fill(-1, 1, 0, -1, 3, 1, LOG))
    L.append(fill(2, 1, 0, 2, 3, 1, LOG))
    L.append(fill(0, 1, -1, 1, 3, -1, LOG))
    L.append(fill(0, 1, 2, 1, 3, 2, LOG))
    for y in range(10, H + 4):
        d = H + 3 - y
        r = min(7, 1 + d // 3)
        if d % 4 == 0:
            r = max(1, r - 1)
        L.append(fill(-r, y, -r + 1, 1 + r, y, 2 + r - 1, LEAF, "keep"))
        L.append(fill(-r + 1, y, -r, 1 + r - 1, y, 2 + r, LEAF, "keep"))
    L.append(fill(0, H + 4, 0, 1, H + 5, 1, LEAF, "keep"))
    L.append(fill(0, 1, 0, 1, H, 1, LOG))
    return L

# --------------------------------------------------------------------------
# the creature's skin, 64x64, written straight out as a PNG
# --------------------------------------------------------------------------
def texture():
    W = H = 64
    px = [[(0, 0, 0, 0) for _ in range(W)] for _ in range(H)]
    rng = random.Random(5)

    def box(u, v, w, h, d, shade):
        """Paint every face of one box in the model, so no part is left blank."""
        faces = [(u + d, v, w, d), (u + d + w, v, w, d),
                 (u, v + d, d, h), (u + d, v + d, w, h),
                 (u + d + w, v + d, d, h), (u + d + w + d, v + d, w, h)]
        for (fu, fv, fw, fh) in faces:
            for y in range(fv, min(fv + fh, H)):
                for x in range(fu, min(fu + fw, W)):
                    n = rng.randint(-3, 3)
                    px[y][x] = (max(0, shade + n), max(0, shade + n), max(0, shade + n + 1), 255)

    box(0, 0, 7, 7, 7, 11)        # head
    box(28, 0, 6, 16, 3, 14)      # body
    box(0, 22, 2, 22, 2, 9)       # arm
    box(12, 22, 2, 12, 2, 12)     # leg
    box(24, 22, 2, 7, 2, 4)       # claw, nearly black

    # the mouth: a circle on the front face of the head, which sits at 7,7
    cx, cy, r = 7 + 3.5, 7 + 4.0, 2.2
    for y in range(7, 14):
        for x in range(7, 14):
            if (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2 <= r * r:
                px[y][x] = (236, 232, 222, 255)
    for y in range(7, 14):                       # a darker rim round it
        for x in range(7, 14):
            d2 = (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2
            if r * r < d2 <= (r + 0.9) ** 2:
                px[y][x] = (36, 22, 22, 255)

    raw = b""
    for row in px:
        raw += b"\x00" + b"".join(struct.pack("BBBB", *p) for p in row)

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    return png

def write(path, lines):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("%-52s %5d lines" % (os.path.relpath(path, HERE), len(lines)))

write(os.path.join(BP, "functions", "bunker", "build.mcfunction"), bunker())
write(os.path.join(BP, "functions", "bunker", "loot.mcfunction"), loot())
write(os.path.join(BP, "functions", "tree", "giant.mcfunction"), giant_spruce())

tex = os.path.join(RP, "textures", "entity", "hunter.png")
os.makedirs(os.path.dirname(tex), exist_ok=True)
open(tex, "wb").write(texture())
print("%-52s %5d bytes" % (os.path.relpath(tex, HERE), os.path.getsize(tex)))
