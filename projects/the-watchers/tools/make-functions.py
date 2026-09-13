#!/usr/bin/env python3
"""
Builds the .mcfunction files that are made of shapes: the bunker and the giant
spruce. Minecraft has no command for a circle, so the circles here are worked
out in Python and written out as a long list of fill commands.

Run it from the project folder:

    python3 tools/make-functions.py

It only writes the generated files listed at the bottom. Everything else in
java/ is written by hand.
"""
import math, os, random

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JAVA = os.path.join(HERE, "java", "data", "watchers", "function")

# --------------------------------------------------------------------------
# little helpers. every coordinate is relative (~) to wherever the function is
# run from, so one function builds a bunker anywhere in the world.
# --------------------------------------------------------------------------
def rel(v):
    return "~" if v == 0 else "~%d" % v

def fill(x1, y1, z1, x2, y2, z2, block, mode=""):
    line = "fill %s %s %s %s %s %s %s" % (
        rel(x1), rel(y1), rel(z1), rel(x2), rel(y2), rel(z2), block)
    return line + (" " + mode if mode else "")

def setb(x, y, z, block):
    return "setblock %s %s %s %s" % (rel(x), rel(y), rel(z), block)

def diwt_rows(cx, cz, r):
    """One (z, x1, x2) span per row of a filled circle."""
    rows = []
    for z in range(cz - r, cz + r + 1):
        dz = z - cz
        half = int((r * r - dz * dz) ** 0.5)
        rows.append((z, cx - half, cx + half))
    return rows

def cylinder(cx, cz, r, y1, y2, block, mode=""):
    return [fill(x1, y1, z, x2, y2, z, block, mode) for z, x1, x2 in diwt_rows(cx, cz, r)]

def ellipsoid(cx, cy, cz, rx, ry, rz, block, mode=""):
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
            if half >= 0:
                out.append(fill(cx - half, y, z, cx + half, y, z, block, mode))
    return out

# --------------------------------------------------------------------------
# THE BUNKER
#
# Run from the block on the surface at the middle of the stone brick circle.
#   y  0     the surface circle
#   y -22    the floor of every room down below
#   y -16    the ceiling
# The round room sits to the north west of the ladder so the ladder does not
# come down on top of the cylinder in the middle of it.
# --------------------------------------------------------------------------
FLOOR, CEIL = -22, -16          # the solid layers
IN_LO, IN_HI = -21, -17         # the air between them
RC_X, RC_Z = -5, -5             # middle of the round room
R_IN, R_OUT = 10, 11            # its inside and outside radius

BRICK = "minecraft:stone_bricks"
AIR = "minecraft:air"

def bunker():
    L = ["# built by tools/make-functions.py — do not edit by hand",
         "# the abandoned bunker: a circle on the surface, four rooms below"]

    # ---- solid stone first, everything gets hollowed out afterwards ----
    L.append("# solid block of stone brick, carved out below")
    L += cylinder(RC_X, RC_Z, R_OUT, FLOOR, CEIL, BRICK)
    # north room shell
    L.append(fill(-15, FLOOR, -35, 5, CEIL, -16, BRICK))
    # east room shell
    L.append(fill(6, FLOOR, -13, 23, CEIL, 3, BRICK))
    # south room shell
    L.append(fill(-9, FLOOR, 6, -1, CEIL, 17, BRICK))
    # west corridor shell
    L.append(fill(-20, FLOOR, -8, -16, CEIL, -2, BRICK))

    # ---- hollow out the round room ----
    L.append("# hollow out the round room")
    L += cylinder(RC_X, RC_Z, R_IN, IN_LO, IN_HI, AIR)
    L.append("# the cylinder standing in the middle of it")
    L += cylinder(RC_X, RC_Z, 3, IN_LO, IN_HI, BRICK)
    L += cylinder(RC_X, RC_Z, 3, IN_HI, IN_HI, "minecraft:chiseled_stone_bricks")
    L.append(fill(RC_X - 1, IN_LO + 1, RC_Z - 4, RC_X + 1, IN_LO + 1, RC_Z - 4,
                  "minecraft:iron_block"))

    # ---- the four corridors and rooms ----
    L.append("# north: the store room, two rows of double chests")
    L.append(fill(-5, IN_LO, -20, -5, IN_LO + 1, -16, AIR))     # corridor
    L.append(fill(-14, IN_LO, -34, 4, IN_HI, -20, AIR))          # the room

    L.append("# east: collapsed")
    L.append(fill(6, IN_LO, -5, 9, IN_LO + 1, -5, AIR))
    L.append(fill(10, IN_LO, -12, 22, IN_HI, 2, AIR))

    L.append("# south: one small room with one chest in it")
    L.append(fill(-5, IN_LO, 6, -5, IN_LO + 1, 10, AIR))
    L.append(fill(-8, IN_LO, 11, -2, IN_HI, 16, AIR))

    L.append("# west: the corridor opens straight into a cave")
    L.append(fill(-19, IN_LO, -5, -16, IN_LO + 1, -5, AIR))

    # ---- the huge cave behind the west door ----
    L.append("# the huge cave")
    L += ellipsoid(-34, -24, -5, 14, 9, 12, AIR)
    L.append(fill(-24, IN_LO, -5, -20, IN_LO + 1, -5, AIR))   # link it to the corridor

    # ---- the collapse in the east room ----
    rng = random.Random(7)
    L.append("# rubble where the east room fell in")
    for i in range(70):
        x = rng.randint(10, 22)
        z = rng.randint(-12, 2)
        h = rng.randint(1, 5)
        block = rng.choice(["minecraft:cobblestone", "minecraft:gravel",
                            "minecraft:stone", "minecraft:cracked_stone_bricks",
                            "minecraft:andesite"])
        L.append(fill(x, IN_LO, z, x, IN_LO + h - 1, z, block))
    L.append(fill(13, IN_LO, -6, 19, IN_HI, 0, "minecraft:cobblestone"))
    L.append(fill(7, IN_LO, -5, 9, IN_LO + 1, -5, "minecraft:gravel"))

    # ---- the way in from the surface ----
    L.append("# the shaft down from the trapdoor")
    L.append(fill(0, -1, 0, 0, -17, 0, AIR))
    L.append(fill(1, IN_LO, 0, 1, IN_HI, 0, BRICK))    # something for the ladder to hang on
    L.append(fill(0, -1, 0, 0, IN_LO, 0, "minecraft:ladder[facing=west]"))

    L.append("# the circle of stone bricks on the surface")
    L += cylinder(0, 0, 6, 0, 0, BRICK)
    L.append(fill(-7, 1, -7, 7, 4, 7, AIR))            # clear whatever grew on top
    for z, x1, x2 in diwt_rows(0, 0, 6):
        for x in (x1, x2):
            if abs(x) + abs(z) >= 6:
                L.append(setb(x, 1, z, "minecraft:iron_bars"))
    for x, z in [(0, -6), (0, 6), (-6, 0), (6, 0)]:
        L.append(setb(x, 1, z, "minecraft:iron_bars"))
    L.append(setb(0, 0, 0, "minecraft:iron_trapdoor[half=bottom,facing=north]"))

    # ---- four iron doors, one in each direction ----
    L.append("# the four doors")
    for (x, z, facing) in [(-5, -16, "north"), (-5, 6, "south"),
                           (6, -5, "east"), (-16, -5, "west")]:
        L.append(setb(x, IN_LO, z, "minecraft:iron_door[half=lower,facing=%s]" % facing))
        L.append(setb(x, IN_LO + 1, z, "minecraft:iron_door[half=upper,facing=%s]" % facing))
    for (x, z, f) in [(-5, -15, "south"), (-5, -17, "north"),
                      (-5, 5, "north"), (-5, 7, "south"),
                      (5, -5, "west"), (7, -5, "east"),
                      (-15, -5, "east"), (-17, -5, "west")]:
        L.append(setb(x, IN_LO + 1, z, "minecraft:stone_button[face=wall,facing=%s]" % f))

    # ---- the chests in the north room ----
    L.append("# two rows of double chests")
    for row_z in (-25, -30):
        for i, x in enumerate((-11, -7, -3, 1)):
            L.append(setb(x, IN_LO, row_z, "minecraft:chest[facing=south,type=right]"))
            L.append(setb(x + 1, IN_LO, row_z, "minecraft:chest[facing=south,type=left]"))

    # ---- the chest in the south room ----
    L.append(setb(-5, IN_LO, 13, "minecraft:chest[facing=north,type=single]"))

    # ---- a very little light, and some age ----
    rng = random.Random(11)
    for i in range(16):
        x = rng.randint(RC_X - 8, RC_X + 8)
        z = rng.randint(RC_Z - 8, RC_Z + 8)
        L.append(setb(x, CEIL - 1, z, "minecraft:soul_lantern[hanging=true]"))
    for i in range(90):
        x = rng.randint(-16, 22)
        z = rng.randint(-34, 16)
        y = rng.choice([FLOOR, CEIL])
        L.append("execute if block %s %s %s %s run %s" % (
            rel(x), rel(y), rel(z), BRICK,
            setb(x, y, z, rng.choice(["minecraft:cracked_stone_bricks",
                                      "minecraft:mossy_stone_bricks"]))))

    L.append("# remember that a bunker stands here, so another is not built on top")
    L.append("summon marker ~ ~ ~ {Tags:[\"wt_bunker\"]}")
    L.append("function watchers:bunker/loot")
    return L

# --------------------------------------------------------------------------
# what is in the chests
# --------------------------------------------------------------------------
FOOD = ["minecraft:cooked_beef", "minecraft:cooked_porkchop", "minecraft:bread",
        "minecraft:cooked_chicken", "minecraft:baked_potato", "minecraft:cooked_cod"]
GEAR = ["minecraft:iron_sword", "minecraft:iron_pickaxe", "minecraft:iron_axe",
        "minecraft:iron_shovel", "minecraft:iron_helmet", "minecraft:iron_chestplate",
        "minecraft:iron_leggings", "minecraft:iron_boots"]
WORN = {"minecraft:iron_sword": 250, "minecraft:iron_pickaxe": 250,
        "minecraft:iron_axe": 250, "minecraft:iron_shovel": 250,
        "minecraft:iron_helmet": 165, "minecraft:iron_chestplate": 240,
        "minecraft:iron_leggings": 225, "minecraft:iron_boots": 195}

def loot():
    rng = random.Random(23)
    L = ["# built by tools/make-functions.py — do not edit by hand",
         "# what is left in the bunker: scraps of food and worn out iron"]
    for row_z in (-25, -30):
        for x in (-11, -7, -3, 1):
            for half in (0, 1):
                items = []
                slots = rng.sample(range(27), rng.randint(3, 7))
                for slot in slots:
                    roll = rng.random()
                    if roll < 0.45:
                        food = rng.choice(FOOD)
                        items.append('{Slot:%db,id:"%s",count:%d}' % (slot, food, rng.randint(1, 6)))
                    elif roll < 0.8:
                        gear = rng.choice(GEAR)
                        dmg = int(WORN[gear] * rng.uniform(0.55, 0.92))
                        items.append('{Slot:%db,id:"%s",count:1,components:{"minecraft:damage":%d}}'
                                     % (slot, gear, dmg))
                    else:
                        items.append('{Slot:%db,id:"minecraft:cobblestone",count:%d}'
                                     % (slot, rng.randint(8, 41)))
                L.append("data merge block %s %s %s {Items:[%s]}" % (
                    rel(x + half), rel(IN_LO), rel(row_z), ",".join(items)))

    page1 = "It hunts at night, It tasted first blood, and now we cannot return."
    page2 = "It hunts as night, It tasted flesh, and now we cannot return."
    page3 = "It hunts at night, it tasted prey, and now we cannot return."
    L.append("# the book and quill in the small room to the south")
    L.append('data merge block %s %s %s {Items:[{Slot:13b,id:"minecraft:writable_book",count:1,'
             'components:{"minecraft:writable_book_content":{pages:["%s","%s","%s"]}}}]}'
             % (rel(-5), rel(IN_LO), rel(13), page1, page2, page3))
    return L

# --------------------------------------------------------------------------
# A GIANT SPRUCE — a 2x2 trunk about 34 blocks tall with skirts of leaves.
# Run from the block the tree stands on.
# --------------------------------------------------------------------------
LOG = "minecraft:spruce_log[axis=y]"
LEAF = "minecraft:spruce_leaves[persistent=true]"

def giant_spruce():
    H = 34
    L = ["# built by tools/make-functions.py — do not edit by hand",
         "# one giant spruce, far bigger than the ones the game grows"]
    L.append(fill(0, 1, 0, 1, H, 1, LOG))
    L.append(fill(-1, 1, 0, -1, 3, 1, LOG))     # a bit of a root flare
    L.append(fill(2, 1, 0, 2, 3, 1, LOG))
    L.append(fill(0, 1, -1, 1, 3, -1, LOG))
    L.append(fill(0, 1, 2, 1, 3, 2, LOG))
    for y in range(10, H + 4):
        d = H + 3 - y
        r = min(7, 1 + d // 3)
        if d % 4 == 0:
            r = max(1, r - 1)
        # a squared-off disc: one wide fill, then the corners trimmed back
        L.append(fill(-r, y, -r + 1, 1 + r, y, 2 + r - 1, LEAF, "keep"))
        L.append(fill(-r + 1, y, -r, 1 + r - 1, y, 2 + r, LEAF, "keep"))
    L.append(fill(0, H + 4, 0, 1, H + 5, 1, LEAF, "keep"))
    L.append(fill(0, 1, 0, 1, H, 1, LOG))       # keep the trunk clear of leaves
    return L

# --------------------------------------------------------------------------
def write(path, lines):
    full = os.path.join(JAVA, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("%-28s %5d lines" % (path, len(lines)))

write("bunker/build.mcfunction", bunker())
write("bunker/loot.mcfunction", loot())
write("tree/giant.mcfunction", giant_spruce())


# --------------------------------------------------------------------------
# THE WATCHER, on Java
#
# A data pack cannot add a mob, so the shape is built out of block displays —
# blocks with no hitbox, squashed and stretched into limbs, dragged onto an
# invisible zombie every tick.
#
# Two things make this fiddly. The forearms and shins point forwards rather
# than down, which means each one carries a rotation of its own; and there can
# be several Watchers at once, so every part is tagged with the slot number of
# the Watcher it belongs to, or the limbs swap bodies when two stand close
# together.
#
# Sizes are the model's own, in sixteenths of a block, so the two editions
# agree about what it looks like.
# --------------------------------------------------------------------------
SLOTS = 4
U = 1.0 / 16.0                      # one model unit, in blocks

def quat_x(deg):
    a = math.radians(deg) / 2.0
    return (math.sin(a), 0.0, 0.0, math.cos(a))

# name, (width, height, depth) in units, (x, y, z) of the corner, turn about X
PARTS = [
    ("torso",  (10, 26, 6),  (-5, 44, -3),    0,   "black_concrete"),
    ("head",   (13, 12, 13), (-6.5, 74, -6.5), 0,  "black_concrete"),
    ("mouth",  (5, 5, 1),    (-2.5, 78, -7.2), 0,  "white_concrete"),
    ("armul",  (3, 28, 3),   (6, 40, -1.5),   0,   "black_concrete"),
    ("armur",  (3, 28, 3),   (-9, 40, -1.5),  0,   "black_concrete"),
    ("armll",  (3, 26, 3),   (6, 42, -1.5),   -90, "black_concrete"),
    ("armlr",  (3, 26, 3),   (-9, 42, -1.5),  -90, "black_concrete"),
    ("clawl",  (2, 16, 2),   (6.5, 42, -5),   -112, "black_concrete"),
    ("clawr",  (2, 16, 2),   (-8.5, 42, -5),  -112, "black_concrete"),
    ("legul",  (4, 24, 4),   (1, 20, -2),     0,   "black_concrete"),
    ("legur",  (4, 24, 4),   (-5, 20, -2),    0,   "black_concrete"),
    ("legll",  (3, 22, 3),   (1.5, 22, -1.5), -38, "black_concrete"),
    ("leglr",  (3, 22, 3),   (-4.5, 22, -1.5), -38, "black_concrete"),
]

def java_parts(slot):
    L = ["# built by tools/make-functions.py — do not edit by hand",
         "# the body of Watcher number %d" % slot,
         "tag @s add wt_p%d" % slot,
         'summon minecraft:marker ~ ~ ~ {Tags:["wt_aim","wt_p%d"]}' % slot]
    for name, size, corner, turn, block in PARTS:
        w, h, d = (v * U for v in size)
        x, y, z = (v * U for v in corner)
        qx, qy, qz, qw = quat_x(turn)
        bright = "{sky:15,block:15}" if name == "mouth" else "{sky:6,block:0}"
        L.append(
            'summon minecraft:block_display ~ ~ ~ '
            '{Tags:["wt_body","wt_%s","wt_p%d"],block_state:{Name:"minecraft:%s"},'
            'brightness:%s,view_range:4.0f,transformation:{translation:[%.4ff,%.4ff,%.4ff],'
            'scale:[%.4ff,%.4ff,%.4ff],left_rotation:[%.5ff,%.5ff,%.5ff,%.5ff],'
            'right_rotation:[0f,0f,0f,1f]}}'
            % (name, slot, block, bright, x, y, z, w, h, d, qx, qy, qz, qw))
    return L

def java_body(slot):
    L = ["# built by tools/make-functions.py — do not edit by hand",
         "# Drag Watcher %d's body onto it, once a tick." % slot,
         "#",
         "# There is no command for \"turn this to the same angle as that\", so a",
         "# marker is parked eight blocks in front and every part is told to face",
         "# it. rotated ~ 0 keeps the left-right angle and throws away the",
         "# up-and-down one, so the body stays upright.",
         "execute rotated ~ 0 positioned ^ ^ ^8 run tp @e[tag=wt_aim,tag=wt_p%d,limit=1] ~ ~ ~" % slot]
    for name, _, _, _, _ in PARTS:
        L.append("tp @e[tag=wt_%s,tag=wt_p%d,limit=1] ~ ~ ~ facing entity @e[tag=wt_aim,tag=wt_p%d,limit=1]"
                 % (name, slot, slot))
    return L

def java_pick_slot():
    """
    Give this Watcher the first slot nobody else is using.

    Each line has to check two different things: that nobody else holds the
    slot (@e), and that we did not already take an earlier one (@s). Without
    the second check, taking slot one makes the next line think slot two is
    free for us as well, and one Watcher ends up wearing two bodies.
    """
    L = ["# built by tools/make-functions.py — do not edit by hand",
         "# Give this Watcher the first slot nobody else is using."]
    for slot in range(1, SLOTS + 1):
        mine = " ".join("unless entity @s[tag=wt_p%d]" % s for s in range(1, slot))
        guard = (mine + " " if mine else "") + "unless entity @e[tag=wt_p%d]" % slot
        L.append("execute %s run function watchers:creature/parts_%d" % (guard, slot))
    return L

def java_body_pick():
    L = ["# built by tools/make-functions.py — do not edit by hand"]
    for slot in range(1, SLOTS + 1):
        L.append("execute if entity @s[tag=wt_p%d] run function watchers:creature/body_%d" % (slot, slot))
    return L

for slot in range(1, SLOTS + 1):
    write("creature/parts_%d.mcfunction" % slot, java_parts(slot))
    write("creature/body_%d.mcfunction" % slot, java_body(slot))
write("creature/parts.mcfunction", java_pick_slot())
write("creature/body.mcfunction", java_body_pick())
