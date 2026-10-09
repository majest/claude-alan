# New York in Roblox

A Roblox map of Manhattan that a script builds from nothing when the game
starts, with the other boroughs across the water, an invisible border round the
lot, and hills and forest beyond the border so the world does not just stop.

The idea is Alan's. **Not published yet** — Alan will say when it is finished.

## What is in the folder

```
roblox/BuildNewYork.server.lua    the city. A Script, for ServerScriptService.
roblox/Neighbourhood.client.lua   the "you are in Midtown" box. A LocalScript.
new-york.rbxlx                    a Roblox place with both scripts in it (made by tools/build.py)
index.html                        the web page: the map, the steps for Studio, the scripts
tools/build.py                    writes new-york.rbxlx and copies the scripts into index.html
tools/check.py                    runs the scripts in a pretend Roblox and reports mistakes
```

**The two files in `roblox/` are the real thing.** Edit those, then run
`python3 tools/build.py`. Do not edit the scripts inside `index.html` or the
`.rbxlx` by hand; the next build would overwrite them.

## How the city is made

Nothing is placed by hand. The script is mostly tables of numbers, and then
loops that turn them into parts.

- **Coordinates.** Positions are written as avenue units (`a`) and street
  numbers (`s`), because that is how New York thinks. 5th Avenue is `a = 7`,
  34th Street is `s = 34`. Two functions, `xOf` and `zOf`, turn those into
  studs. Below Houston Street the numbers go negative, down to `-26` at the
  Battery, because those streets have names rather than numbers.
- **The shoreline** is sixteen rows of *street number, east edge, west edge*.
  Between rows it is a straight line. A block is built if its centre is
  inside that outline.
- **The grid.** Avenues every 70 studs, streets every 54. One game street
  stands for two real ones; at one-to-one the blocks were too small to walk
  round and there were twice as many parts.
- **Neighbourhoods** are one line each in `ZONES`: where it is, how tall its
  buildings are, which colours and materials it uses. The first line that
  matches a block wins, so the small places (Times Square, the parks) come
  before the big bands (Midtown, Harlem).
- **Landmarks** reserve the blocks they stand on, then build themselves with
  a small function each. The Flatiron is a `WedgePart` turned on its side;
  the Chrysler crown is seven shrinking boxes of metal.
- **Ground and water are terrain**, not parts. Terrain is made of 4-stud
  voxels, so shorelines come out a little blocky, but a whole river costs
  nothing. The parks are grass terrain raised just above the asphalt; the
  lakes are holes dug into it and filled with water.
- **Beyond the border** the hills are balls of terrain sunk most of the way
  into the ground, and the trees find the ground under them with a ray cast
  straight down, so they sit on the hills instead of floating.
- **The client script** gets everything it needs (the shoreline, the zones,
  the grid size) from attributes the server puts in `ReplicatedStorage`, so
  it does not have its own copy of the map to keep in step.

About 6,700 parts in total, and a few seconds to build.

## Checking it without Roblox

```sh
python3 tools/check.py
```

Only Roblox Studio can actually run these scripts, and it is not installed
here. So `check.py` builds a pretend Roblox in plain Lua — `Instance.new`,
`Vector3`, `CFrame`, `Enum`, the terrain functions — and runs the real
scripts on it. It catches the things that actually go wrong: a property
spelt wrong, a material that does not exist, a part over 2048 studs, a
number that came out as `nan`, a table that was `nil`. It also walks a
pretend player to ten spots and prints what the neighbourhood box would say.

It cannot say whether the city *looks* right. Only Studio can.

It needs the `lupa` module: `pip install lupa`.

## Things that are only guessed at

These were decided without seeing the result in Studio, and may want changing
once someone has:

- **The Flatiron's point** should face north. If the wedge comes out pointing
  south, flip the angle in its `build` function.
- **Build time.** The terrain fill covers the whole world, including the sea.
  If the game takes too long to start, turn `BEYOND` down.
- **Water depth** is only 4 studs. If it looks wrong from a bridge, deepen
  the water fill in `buildWater`.

## Still to decide

Nothing needs Artur for this one. Everything here is free, and nothing
touches `.github/`.

- **Should the border be solid?** It is now (`BORDER_SOLID = true`). Alan
  asked for "a border", so that is what it does; set it to `false` to let
  players walk out into the hills. Claude would keep it solid and make the
  hills something to look at, not somewhere to get lost.
- **The border is invisible** because Alan asked for that
  (`BORDER_VISIBLE = false`). The cost is that you cannot see it coming, so
  you find it by walking into it. If that gets annoying, a thin line on the
  ground along the edge would show where it is without a wall in the sky.
