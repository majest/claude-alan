# Extinction

A Minecraft horror mod, written as a **data pack** for Java Edition 1.21 or newer.

The idea, the creature, the bunker and the book are Alan's.

```
index.html      the page: what it does, how to install it, and the download
java/           the data pack itself — this is the real thing, edit these files
tools/          three small scripts, explained below
```

## Why a data pack and not a real mod

A real mod is Java code compiled into a `.jar`, and it needs Java, Gradle and a
modding toolkit to build. A data pack is nothing but text files that Minecraft
already knows how to read, so it needs none of that, and it can be published on
a web page.

The price is that a data pack **cannot add anything new to the game**. It can
only give orders to what is already there. Everything odd about how this is
built comes from working around that:

| What it looks like | What it actually is |
| --- | --- |
| A thin black creature with claws | An invisible zombie with block displays stuck to it every tick |
| It climbs walls | A check for a wall in front, and a shove upwards |
| Its tongue grabs you | You get teleported a fraction of a block towards it, twenty times a second |
| Animals with black eyes | Animals glowing black, because eyes need a texture pack |
| A new spruce biome | Giant spruces built by command around each bunker |

## The three tools

Run them from this folder.

```sh
python3 tools/check.py           # look for mistakes without opening Minecraft
python3 tools/make-functions.py  # rebuild the shapes: the bunker and the tree
python3 tools/embed-pack.py      # copy java/ into index.html for the download
```

**`check.py`** catches the three mistakes that actually happen: a function
calling one that does not exist, a tag that was never written, and a scoreboard
that was never created. It cannot tell you whether Minecraft likes a command.

**`make-functions.py`** writes `bunker/build.mcfunction`,
`bunker/loot.mcfunction` and `tree/giant.mcfunction`. Minecraft has no command
for a circle, so the circles are worked out in Python and written out as a long
list of `fill` commands. **Do not edit those three files by hand** — change the
Python and run it again.

**`embed-pack.py`** copies every file in `java/` into `index.html`, so the page
can build the download with no server behind it. It rewrites the block between
the `PACK DATA` markers. **Do not edit that block by hand.**

After changing anything in `java/`, run `check.py` and then `embed-pack.py`, or
the download will still contain the old version.

## How it fits together

`load.mcfunction` runs once when the world loads and makes the scoreboards.
`tick.mcfunction` runs twenty times a second and is deliberately short: it
works out the day and the time, moves the creature's body, and hands everything
else to `second.mcfunction`, which runs once a second.

The day number comes from `time query day`, and the day drives everything:

| Day | Function |
| --- | --- |
| 2 | `creature/spawn` — one creature, at night, never two |
| 3 | `mobs/turn` — a few more animals turn every second |
| 5 | `mobs/cull` and `stopsound @a music` |
| 6 | `mobs/swarm` |

`place/ground` is worth reading. It is a function that calls itself, stepping
down one block at a time until it finds something solid, and it is how the
creature, the extra mobs, the bunkers and the trees all find the ground.

## Still to decide

- **Bedrock.** Not built. Bedrock uses behaviour packs, which are a different
  set of files with a different shape, so it is a second port rather than a
  copy.
- **Black eyes** need a texture pack. That means editing Minecraft's own
  pictures, which has to be done by hand.
- **Nothing here has been tested in the game.** It was written on a computer
  with no Minecraft installed. The checker says the pack is put together
  correctly; it cannot say whether it is any good, or whether every command is
  spelled the way this version of Minecraft wants.
