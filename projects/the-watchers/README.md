# The Watchers

A Minecraft horror mod, built twice: a **data pack** for Java Edition and an
**add-on** for Bedrock Edition.

The Watchers is the fear of being looked at, which is what the creature does to
you. Look back at it and it knows, and it starts running.

The idea, the timeline, the creature, the bunker and the book are Alan's.

## What it is

They only come out at night. In daylight there are none of them at all: they
arrive after dark, and any still standing at sunrise are taken away.

For two days nothing chases you. After dark something simply turns up beside you
and stands there. Three times your height, thin, black, with arms that bend the wrong way
and no face at all except one round white mouth.

It does not move while you are looking at it. Look straight at it and it knows,
and it comes. Run, turn round, and it is not there — it was not hiding, it was
taken away, and another will be standing somewhere else in a minute.

| Day | What changes |
| --- | --- |
| 1–2 | After dark they turn up beside you and watch. They do not move, and they are gone the moment you look away. |
| 3 | That night they stop watching. They come for you and for your base, and from now on every night they arrive already hunting. |
| 4 | Almost no animals left. The ones there are have black eyes, come for you, and their legs stretch as they run. |
| 5 | The music stops. |
| 6 | More of them, every night, for good. |

Now and then one skips the watching and is simply standing three blocks in front
of your face for a second, with a roar and the camera shaking. It does no damage.
There is a two minute cooldown on those per player, because a jumpscare you can
predict is not one.

The old spruce forests have fog, cobwebs in the canopy, and several times the
usual number of Watchers; stand still in one for a minute and one will find you.
Most villages are empty by the time you reach them. And somewhere within a
thousand blocks of spawn, somebody built a bunker and did not come back out;
after that they get further and further apart.

## Why not a real mod

A real mod is Java code compiled into a `.jar` and it needs a whole toolchain to
build. A data pack and an add-on are files Minecraft already knows how to read,
so they need none of that, and they can be published on a web page.

## The two editions are not the same build

They cannot be. Nothing is shared between them. Same idea, written twice.
Bedrock wins most of these, because Bedrock can add a real mob and Java cannot.

| | Java | Bedrock |
| --- | --- | --- |
| The creature | An invisible zombie scaled up three times wearing thirteen block displays, dragged onto it every tick | A real custom mob with its own model, skin and animation |
| Its forearms | Fixed, pointing forward | Jointed, and animated separately from the upper arm |
| Climbing | Faked: check for a wall, shove upwards | `minecraft:can_climb`, the component spiders use |
| Breaking blocks | A block tag and `setblock ... destroy` | `minecraft:break_blocks`, plus the manual check as a backup |
| Fog in the forest | **No.** A data pack cannot touch fog | A real fog setting, pushed and popped as you walk in and out |
| Black eyes | **No.** The turned animals glow black round the edges | A mob of our own with black eyes painted on |
| Legs stretching | **No.** | The leg bones scale with running speed |
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

## The six tools

Run them from this folder.

```sh
python3 tools/check.py            # look for mistakes without opening Minecraft
python3 tools/make-functions.py   # rebuild the Java bunker and tree
python3 tools/make-bedrock.py     # rebuild the Bedrock bunker, tree and texture
python3 tools/render-creature.py  # draw the creature from its own model file
python3 tools/embed-pack.py       # copy both packs into index.html
python3 tools/build-downloads.py  # write the two files the page links to
python3 tools/make-icon.py        # redraw the pack icon
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

**`make-icon.py`** draws the pack icon — the picture Minecraft shows beside the
pack in its list. It is drawn at 64x64 and blown up with no smoothing, so every
pixel stays a hard square and it looks like it belongs in the game. It writes
four copies, because the two editions want different names in different places:
`java/pack.png`, a `pack_icon.png` in each half of the add-on, and one for the
website.

**`build-downloads.py`** writes `the-watchers.mcaddon` and
`the-watchers-java.zip` next to `index.html`. The page can build both inside the
browser too, but a file built by JavaScript arrives as a blob and browsers do
awkward things to blobs — Safari unzips them, others rename them to `.zip`, and
a renamed `.mcaddon` will not open in Minecraft. A real file on the website is
just a file. Both exist; the links point at the real files and the buttons are
the fallback.

After changing anything in `java/` or `bedrock/`, run `embed-pack.py` **and**
`build-downloads.py`, then `check.py` — which now refuses to pass if either
download is out of date with the folder it came from.

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
| `watchers_bp/manifest.json` | `@minecraft/server` `1.11.0` | `2.9.0` | The `1.x` line ended at `1.19.0`. Asking for a version that no longer exists is enough on its own to stop a pack installing. |
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
