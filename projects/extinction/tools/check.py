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

unused = functions - {n for n, _, _ in used_fn} - {"extinction:load", "extinction:tick"}
print("%d functions, %d tags, %d json files" % (len(functions), len(tags), len(jsons)))
if unused:
    print("never called:", ", ".join(sorted(unused)))
if problems:
    print("\n%d problem(s):" % len(problems))
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("no problems found")
