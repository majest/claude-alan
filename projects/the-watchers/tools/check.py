#!/usr/bin/env python3
"""
Checks the data pack without Minecraft.

It cannot tell you whether the game likes a command, but it catches the three
mistakes that actually happen: a function calling one that does not exist, a
tag that was never written, and a scoreboard that was never created.

    python3 tools/check.py
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JAVA = os.path.join(HERE, "java")
problems = []

# ---- every json file has to parse, or the whole pack refuses to load ----
jsons = []
for dp, dn, fn in os.walk(JAVA):
    for f in fn:
        if f.endswith(".json") or f.endswith(".mcmeta"):
            full = os.path.join(dp, f)
            jsons.append(full)
            try:
                json.load(open(full, encoding="utf-8"))
            except Exception as e:
                problems.append("%s is not valid JSON: %s" % (os.path.relpath(full, HERE), e))

# ---- collect what exists ----
functions, tags = set(), set()
for dp, dn, fn in os.walk(JAVA):
    for f in fn:
        full = os.path.join(dp, f)
        rel = os.path.relpath(full, JAVA).replace(os.sep, "/")
        m = re.match(r"data/([a-z_]+)/function/(.+)\.mcfunction$", rel)
        if m:
            functions.add("%s:%s" % (m.group(1), m.group(2)))
        m = re.match(r"data/([a-z_]+)/tags/([a-z_/]+)/(.+)\.json$", rel)
        if m:
            tags.add("%s:%s" % (m.group(1), m.group(3)))

# ---- what gets used ----
objectives = set()
used_obj, used_fn, used_tag = set(), set(), set()
for dp, dn, fn in os.walk(JAVA):
    for f in sorted(fn):
        if not f.endswith(".mcfunction"):
            continue
        full = os.path.join(dp, f)
        rel = os.path.relpath(full, HERE)
        for i, line in enumerate(open(full, encoding="utf-8"), 1):
            line = line.rstrip("\n")
            if line.startswith("#") or not line.strip():
                continue
            if "\t" in line:
                problems.append("%s line %d has a tab in it" % (rel, i))
            for m in re.finditer(r"scoreboard objectives add (\S+)", line):
                objectives.add(m.group(1))
            for m in re.finditer(r"function ([a-z_]+:[a-z_0-9/]+)", line):
                used_fn.add((m.group(1), rel, i))
            for m in re.finditer(r"#([a-z_]+:[a-z_0-9/]+)", line):
                if not m.group(1).startswith("minecraft:"):
                    used_tag.add((m.group(1), rel, i))
            for m in re.finditer(r"scoreboard players \w+ \S+ (\S+)", line):
                used_obj.add((m.group(1), rel, i))
            for m in re.finditer(r"(?:if|unless) score \S+ (\S+)", line):
                used_obj.add((m.group(1), rel, i))
            for m in re.finditer(r"store result score \S+ (\S+)", line):
                used_obj.add((m.group(1), rel, i))

for name, rel, i in sorted(used_fn):
    if name not in functions:
        problems.append("%s line %d calls %s, which does not exist" % (rel, i, name))
for name, rel, i in sorted(used_tag):
    short = name.split(":")[1].split("/")[-1]
    if not any(t.endswith(":" + short) for t in tags):
        problems.append("%s line %d uses tag #%s, which does not exist" % (rel, i, name))
for name, rel, i in sorted(used_obj):
    if name not in objectives:
        problems.append("%s line %d uses scoreboard %s, which is never created" % (rel, i, name))

unused = functions - {n for n, _, _ in used_fn} - {"watchers:load", "watchers:tick"}
print("%d functions, %d tags, %d json files" % (len(functions), len(tags), len(jsons)))
if unused:
    print("never called:", ", ".join(sorted(unused)))
if problems:
    print("\n%d problem(s):" % len(problems))
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("java: no problems found")

# ---------------------------------------------------------------------------
# the Bedrock add-on
# ---------------------------------------------------------------------------
BED = os.path.join(HERE, "bedrock")
bed = []
if os.path.isdir(BED):
    packs = {}
    for dp, dn, fn in os.walk(BED):
        for f in fn:
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, HERE)
            if f.endswith(".json"):
                try:
                    packs[rel] = json.load(open(full, encoding="utf-8"))
                except Exception as e:
                    bed.append("%s is not valid JSON: %s" % (rel, e))

    def find(tail):
        for k in packs:
            if k.replace(os.sep, "/").endswith(tail):
                return k, packs[k]
        return None, None

    bpk, bp = find("watchers_bp/manifest.json")
    rpk, rp = find("watchers_rp/manifest.json")
    ek, ent = find("entities/watcher.json")
    ck, cli = find("entity/watcher.entity.json")
    gk, geo = find("models/entity/watcher.geo.json")
    rck, rc = find("render_controllers/watcher.render.json")
    ak, anim = find("animations/watcher.animation.json")

    for name, obj in [("behaviour manifest", bp), ("resource manifest", rp),
                      ("entity", ent), ("client entity", cli),
                      ("geometry", geo), ("render controller", rc),
                      ("animation", anim)]:
        if obj is None:
            bed.append("the Bedrock %s is missing" % name)

    if bp and rp:
        ids = [bp["header"]["uuid"]] + [m["uuid"] for m in bp["modules"]]
        ids += [rp["header"]["uuid"]] + [m["uuid"] for m in rp["modules"]]
        if len(set(ids)) != len(ids):
            bed.append("two Bedrock packs share a uuid — Minecraft will load only one")
        dep = [d.get("uuid") for d in bp.get("dependencies", [])]
        if rp["header"]["uuid"] not in dep:
            bed.append("the behaviour pack does not depend on the resource pack")
        entry = [m for m in bp["modules"] if m["type"] == "script"]
        if entry:
            script = os.path.join(BED, "watchers_bp", entry[0]["entry"])
            if not os.path.exists(script):
                bed.append("the manifest points at %s, which is not there" % entry[0]["entry"])

    # Minecraft renumbered itself in 2026: what the launcher calls 26.45 is
    # engine 1.26.45, the leading 1 simply dropped. Two numbers went stale with
    # it and stopped the add-on installing at all, so they are checked here.
    # Both were looked up on 13 September 2026; if they rot, look them up again
    # rather than guessing.
    if bp:
        for d in bp.get("dependencies", []):
            if d.get("module_name") == "@minecraft/server":
                major = str(d.get("version", "")).split(".")[0]
                if major == "1":
                    bed.append("the script asks for @minecraft/server 1.x, and that "
                               "line ended at 1.19.0 — the game is on 2.x now")
        mev = bp["header"].get("min_engine_version", [0, 0, 0])
        if mev[0] == 1 and mev[1] < 25:
            bed.append("min_engine_version is %s, which is more than one version "
                       "behind the engine (1.26.x) and may be refused" % mev)
        if mev[0] > 1:
            bed.append("min_engine_version is %s — the engine still reports major "
                       "version 1, so this should be [1, 26, 0], not the number "
                       "the launcher shows" % mev)

    # the same checks again for every other mob in the pack
    for other in ("turned",):
        ok, oent = find("entities/%s.json" % other)
        ck2, ocli = find("entity/%s.entity.json" % other)
        gk2, ogeo = find("models/entity/%s.geo.json" % other)
        ak2, oanim = find("animations/%s.animation.json" % other)
        if not (oent and ocli and ogeo and oanim):
            bed.append("%s is missing one of its four files" % other)
            continue
        if oent["minecraft:entity"]["description"]["identifier"] != \
           ocli["minecraft:client_entity"]["description"]["identifier"]:
            bed.append("%s: the behaviour and the look disagree about its name" % other)
        want = ocli["minecraft:client_entity"]["description"]["geometry"]["default"]
        if want != ogeo["minecraft:geometry"][0]["description"]["identifier"]:
            bed.append("%s asks for model %s, which is not what the model is called" % (other, want))
        tex2 = ocli["minecraft:client_entity"]["description"]["textures"]["default"]
        if not os.path.exists(os.path.join(BED, "watchers_rp", tex2 + ".png")):
            bed.append("%s: the texture %s.png is missing" % (other, tex2))
        bones = set()
        for b in ogeo["minecraft:geometry"][0]["bones"]:
            bones.add(b["name"])
        for a2 in oanim["animations"].values():
            for bone in a2.get("bones", {}):
                if bone not in bones:
                    bed.append("%s: the animation moves bone %s, which the model does not have"
                               % (other, bone))
        for key, name in ocli["minecraft:client_entity"]["description"].get("animations", {}).items():
            if name not in oanim["animations"]:
                bed.append("%s: animation %s is used but never defined" % (other, name))

    if ent and cli:
        a = ent["minecraft:entity"]["description"]["identifier"]
        b = cli["minecraft:client_entity"]["description"]["identifier"]
        if a != b:
            bed.append("the entity is %s but the client entity is %s" % (a, b))
    if cli and geo:
        want = cli["minecraft:client_entity"]["description"]["geometry"]["default"]
        have = geo["minecraft:geometry"][0]["description"]["identifier"]
        if want != have:
            bed.append("the client entity asks for %s but the model is %s" % (want, have))
        tex = cli["minecraft:client_entity"]["description"]["textures"]["default"]
        if not os.path.exists(os.path.join(BED, "watchers_rp", tex + ".png")):
            bed.append("the texture %s.png is missing" % tex)
    if cli and anim:
        for key, name in cli["minecraft:client_entity"]["description"].get("animations", {}).items():
            if name not in anim["animations"]:
                bed.append("animation %s is used but never defined" % name)
    if geo and anim:
        names = set()
        for b in geo["minecraft:geometry"][0]["bones"]:
            names.add(b["name"])
            if "parent" in b and b["parent"] not in names:
                bed.append("bone %s has parent %s, which comes later or not at all"
                           % (b["name"], b["parent"]))
        for a in anim["animations"].values():
            for bone in a.get("bones", {}):
                if bone not in names:
                    bed.append("the animation moves bone %s, which the model does not have" % bone)

# ---------------------------------------------------------------------------
# are the two download files still the same as the folders they came from?
# a stale download is worse than no download: it looks like it worked.
# ---------------------------------------------------------------------------
import zipfile
for folder, archive in (("java", "the-watchers-java.zip"),
                        ("bedrock", "the-watchers.mcaddon")):
    path = os.path.join(HERE, archive)
    root = os.path.join(HERE, folder)
    if not os.path.exists(path):
        bed.append("%s has not been built — run tools/build-downloads.py" % archive)
        continue
    have = {}
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if f.startswith("."):
                continue
            full = os.path.join(dp, f)
            have[os.path.relpath(full, root).replace(os.sep, "/")] = open(full, "rb").read()
    with zipfile.ZipFile(path) as z:
        inside = {n: z.read(n) for n in z.namelist()}
    if inside != have:
        bed.append("%s is out of date — run tools/build-downloads.py" % archive)

print("bedrock: %d json files" % len(packs))
if bed:
    print("\n%d Bedrock problem(s):" % len(bed))
    for p in bed:
        print("  -", p)
    sys.exit(1)
print("bedrock looks put together correctly")
