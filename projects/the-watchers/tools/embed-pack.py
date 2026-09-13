#!/usr/bin/env python3
"""
Copies every file of the data pack into index.html, so the page can build the
download with no server and no internet behind it.

The files in java/ are the real thing — edit those. Then run:

    python3 tools/embed-pack.py

and it rewrites the block between the PACK DATA markers in index.html. Never
edit that block by hand; it gets overwritten.
"""
import base64, json, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = "/* PACK DATA START */"
END = "/* PACK DATA END */"

def collect(folder):
    root = os.path.join(HERE, folder)
    if not os.path.isdir(root):
        return {}
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for name in sorted(filenames):
            if name.startswith("."):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            raw = open(full, "rb").read()
            try:
                out[rel] = raw.decode("utf-8")
            except UnicodeDecodeError:
                # a picture, not text — carry it as base64 and let the page
                # turn it back into bytes when it builds the download
                out[rel] = {"b64": base64.b64encode(raw).decode("ascii")}
    return out

pack = {"java": collect("java")}
if collect("bedrock"):
    pack["bedrock"] = collect("bedrock")

blob = json.dumps(pack, indent=0, ensure_ascii=False)
page = os.path.join(HERE, "index.html")
text = open(page, encoding="utf-8").read()
a = text.index(START) + len(START)
b = text.index(END)
text = text[:a] + "\nconst PACK = " + blob + ";\n" + text[b:]
open(page, "w", encoding="utf-8").write(text)

for kind, files in pack.items():
    size = sum(len(v) if isinstance(v, str) else len(v["b64"]) for v in files.values())
    print("%-8s %3d files, %6.1f KB" % (kind, len(files), size / 1024))
print("index.html is now %.1f KB" % (len(text) / 1024))
