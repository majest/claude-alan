#!/usr/bin/env python3
"""
Builds the two download files and puts them next to index.html.

    python3 tools/build-downloads.py

The page can already build these in your browser out of the copies stored
inside it, and that still works. But a file built by JavaScript arrives as a
blob, and browsers do awkward things to blobs: Safari unzips them on the way
in, some browsers rename them to .zip, and a phone may refuse to save one at
all. A real file sitting on the website is just a file, and every browser
knows what to do with it.

So both exist. The links point at these; the buttons are the fallback.
"""

import os, zipfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def build(source, out, note):
    root = os.path.join(HERE, source)
    path = os.path.join(HERE, out)
    files = []
    for dp, dn, fn in os.walk(root):
        dn[:] = sorted(d for d in dn if not d.startswith("."))
        for name in sorted(fn):
            if name.startswith("."):
                continue
            full = os.path.join(dp, name)
            files.append((full, os.path.relpath(full, root).replace(os.sep, "/")))

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for full, rel in files:
            z.write(full, rel)

    print("%-26s %3d files  %6.1f KB   %s" % (out, len(files),
                                              os.path.getsize(path) / 1024, note))

build("java", "the-watchers-java.zip",
      "drop into a world's datapacks folder")
build("bedrock", "the-watchers.mcaddon",
      "open it and Minecraft imports both packs")
