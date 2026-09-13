# Scopophobia

A Minecraft horror mod, built twice: a **data pack** for Java Edition and an
**add-on** for Bedrock Edition.

Scopophobia is the fear of being looked at, which is what the creature does to
you. Look back at it and it knows, and it starts running.

The idea, the timeline, the creature, the bunker and the book are Alan's.

```
index.html      the page: what it does, how to install it, both downloads
java/           the Java data pack — the real thing, edit these files
bedrock/        the Bedrock add-on, in two halves
  scopophobia_bp/   behaviour pack: the entity, the bunker, the script
  scopophobia_rp/   resource pack: the model, the texture, the animation
art/            pictures, and index.json saying what exists
ai/request.json what was asked of the machine at home
tools/          four small scripts, explained below
```

## Why not a real mod

A real mod is Java code compiled into a `.jar` and it needs a whole toolchain to
build. A data pack and an add-on are files Minecraft already knows how to read,
so they need none of that, and they can be published on a web page.

## The two editions are not the same build

They cannot be. Nothing is shared between them. Same idea, written twice.

| | Java | Bedrock |
| --- | --- | --- |
| The creature | An invisible zombie with block displays dragged onto it every tick | A real custom mob with its own model, texture and walking animation |
| Climbing | Faked: check for a wall, shove upwards | `minecraft:can_climb`, the component spiders use |
| Breaking blocks | A block tag and `setblock ... destroy` | `minecraft:break_blocks`, the component ravagers use, with the manual check as a backup |
| The timeline | `.mcfunction` files and scoreboards | JavaScript |
| The book | A book and quill, with the words in it | Three signs, written by the script |
| The way down | A ladder | A spiral staircase |

**Why Bedrock needs a script at all:** Bedrock has no `execute store`, so there
is no way to get the day number out of the game and into a scoreboard. No day
number, no timeline, and the timeline is the whole mod. The scripting API can
simply ask the world what day it is.

**Why Bedrock has no ladders or doors:** Bedrock writes block states
differently from Java and gets them wrong quietly. Everything the bunker places
there is a plain block with no state on it, which is why the way down is a
staircase.

## The four tools

Run them from this folder.

```sh
python3 tools/check.py            # look for mistakes without opening Minecraft
python3 tools/make-functions.py   # rebuild the Java bunker and tree
python3 tools/make-bedrock.py     # rebuild the Bedrock bunker, tree and texture
python3 tools/render-creature.py  # draw the creature from its own model file
python3 tools/embed-pack.py       # copy both packs into index.html
```

**`check.py`** catches the mistakes that actually happen: a function calling one
that does not exist, a tag that was never written, a scoreboard that was never
created, two Bedrock packs sharing a uuid, a model and an animation that
disagree about which bones there are. It cannot tell you whether Minecraft likes
a command.

**`make-functions.py`** and **`make-bedrock.py`** write the files that are made
of shapes. Minecraft has no command for a circle, so the circles are worked out
in Python and written out as long lists of `fill` commands. **Do not edit those
files by hand** — change the Python and run it again.

**`render-creature.py`** reads the same model file the game reads and draws it.
This is here because the image model on the machine at home could not: asked for
a head with no eyes it kept putting eyes on, because nearly every face it has
ever seen has two. Telling an image model *not* to draw something is the thing
it is worst at.

**`embed-pack.py`** copies every file of both packs into `index.html` so the
page can build the downloads with no server behind it. Pictures go in as base64.
It rewrites the block between the `PACK DATA` markers. **Do not edit that block
by hand.**

After changing anything in `java/` or `bedrock/`, run `check.py` and then
`embed-pack.py`, or the downloads will still hold the old version.

## How the Java side fits together

`load.mcfunction` runs once and makes the scoreboards. `tick.mcfunction` runs
twenty times a second and is deliberately short: it works out the day and the
time, moves the creature's body, and hands everything else to `second.mcfunction`.

`place/ground.mcfunction` is worth reading. It is a function that calls itself,
stepping down one block at a time until it finds something solid, and it is how
the creature, the extra mobs, the bunkers and the trees all find the ground.

## Version numbers, and the trap in them

Minecraft renumbered itself in 2026. What the launcher calls **26.45** is engine
**1.26.45** — the leading `1` was simply dropped. Three numbers went stale when
that happened, and two of them stopped the Bedrock add-on installing at all.

| Where | Was | Now | Why |
| --- | --- | --- | --- |
| `scopophobia_bp/manifest.json` | `@minecraft/server` `1.11.0` | `2.9.0` | The `1.x` line ended at `1.19.0`. Asking for a version that no longer exists is enough on its own to stop a pack installing. |
| both Bedrock manifests | `min_engine_version [1, 21, 0]` | `[1, 26, 0]` | Packs more than one minor version behind the engine are treated as out of date. Note it is still `[1, 26, 0]` and not `[26, 45, 0]` — the engine kept its leading 1. |
| `java/pack.mcmeta` | `pack_format` only | also `min_format` / `max_format` | Java changed the shape of this file in 25w31a. The old fields are still there for older games. |
| `scripts/main.js` | `worldInitialize` | `worldLoad` | Renamed when the scripting API went from 1 to 2. Both are tried. |

`tools/check.py` now catches the first two, so it cannot happen quietly again.
All of it was looked up on 13 September 2026; if it rots, look it up again
rather than guessing.

## Still to decide

- **Black eyes** need a texture pack built on Minecraft's own pictures of a cow
  and a pig, painted by hand. Neither edition has them.
- **A real spruce biome** rather than giant trees planted around the bunkers.
  Changing world generation is a much bigger and riskier job.
- **Nothing here has been tested in the game.** It was written on a computer
  with no Minecraft installed. The checker says both packs are put together
  correctly; it cannot say whether they are any good.
