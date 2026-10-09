#!/usr/bin/env python3
"""Put the two Roblox scripts where the page and Studio can get them.

    python3 tools/build.py

1. Writes `new-york.rbxlx`: a Roblox place file with both scripts already in
   the right places. Studio opens it with File > Open from File.
2. Copies both scripts into `index.html`, between the SCRIPTS markers, so the
   page can show them and offer them as downloads with no server behind it.

The scripts in `roblox/` are the real ones. Edit those, then run this.
"""

import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = [
    # (file, name in Studio, class, where it goes)
    ("BuildNewYork.server.lua", "BuildNewYork", "Script", "ServerScriptService"),
    ("Neighbourhood.client.lua", "Neighbourhood", "LocalScript", "StarterPlayerScripts"),
    ("TaxiDriver.client.lua", "TaxiDriver", "LocalScript", "StarterPlayerScripts"),
]


def cdata(text):
    # "]]>" would end the CDATA block early, so split it across two blocks.
    return "<![CDATA[" + text.replace("]]>", "]]]]><![CDATA[>") + "]]>"


def script_item(name, cls, source, ref):
    return (
        f'    <Item class="{cls}" referent="{ref}">\n'
        f'      <Properties>\n'
        f'        <string name="Name">{name}</string>\n'
        f'        <ProtectedString name="Source">{cdata(source)}</ProtectedString>\n'
        f'      </Properties>\n'
        f'    </Item>\n'
    )


def write_place(sources):
    server = [s for s in SCRIPTS if s[3] == "ServerScriptService"]
    client = [s for s in SCRIPTS if s[3] == "StarterPlayerScripts"]
    out = [
        '<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:noNamespaceSchemaLocation="http://www.roblox.com/roblox.xsd" version="4">\n',
        '  <Meta name="ExplicitAutoJoints">true</Meta>\n',
        '  <External>null</External>\n',
        '  <External>nil</External>\n',
        '  <Item class="Workspace" referent="RBX_Workspace">\n',
        '    <Properties><string name="Name">Workspace</string></Properties>\n',
        '  </Item>\n',
        '  <Item class="ServerScriptService" referent="RBX_SSS">\n',
        '    <Properties><string name="Name">ServerScriptService</string></Properties>\n',
    ]
    for i, (file, name, cls, _) in enumerate(server):
        out.append(script_item(name, cls, sources[file], f"RBX_Server{i}"))
    out += [
        '  </Item>\n',
        '  <Item class="StarterPlayer" referent="RBX_StarterPlayer">\n',
        '    <Properties><string name="Name">StarterPlayer</string></Properties>\n',
        '    <Item class="StarterPlayerScripts" referent="RBX_SPS">\n',
        '      <Properties><string name="Name">StarterPlayerScripts</string></Properties>\n',
    ]
    for i, (file, name, cls, _) in enumerate(client):
        out.append(script_item(name, cls, sources[file], f"RBX_Client{i}").replace("\n    ", "\n      "))
    out += [
        '    </Item>\n',
        '  </Item>\n',
        '</roblox>\n',
    ]
    path = HERE / "new-york.rbxlx"
    path.write_text("".join(out), encoding="utf-8")
    print(f"wrote {path.name} ({path.stat().st_size:,} bytes)")


def embed(sources):
    page = HERE / "index.html"
    html = page.read_text(encoding="utf-8")
    begin, end = "<!-- SCRIPTS:BEGIN -->", "<!-- SCRIPTS:END -->"
    if begin not in html or end not in html:
        raise SystemExit("index.html has lost its SCRIPTS markers")
    parts = [begin, "\n<!-- Written by tools/build.py from the files in roblox/. Do not edit here. -->\n"]
    for file, name, cls, _ in SCRIPTS:
        text = sources[file].replace("</script", "<\\/script")
        parts.append(f'<script type="text/plain" id="lua-{name}" data-file="{file}">\n{text}</script>\n')
    parts.append(end)
    html = re.sub(re.escape(begin) + r".*?" + re.escape(end), lambda m: "".join(parts), html, flags=re.S)
    page.write_text(html, encoding="utf-8")
    print(f"embedded {len(SCRIPTS)} scripts into index.html")


def main():
    sources = {file: (HERE / "roblox" / file).read_text(encoding="utf-8") for file, _, _, _ in SCRIPTS}
    write_place(sources)
    embed(sources)


if __name__ == "__main__":
    main()
