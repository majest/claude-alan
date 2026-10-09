# New York in Roblox

A Roblox game. A script builds Manhattan from nothing when the game starts,
with the other boroughs across the water, an invisible border round the lot,
hills and forest beyond it, and yellow taxis to drive. A minute later a
monster comes up out of the harbour, takes the head off the Statue of Liberty
and walks into the city. That is the game.

The idea is Alan's. **Not published yet** — Alan will say when it is finished.

## What is in the folder

```
roblox/BuildNewYork.server.lua    the city. A Script, for ServerScriptService.
roblox/Monster.server.lua         the monster and its parasites. A Script, for ServerScriptService.
roblox/MonsterEffects.client.lua  camera shake, dust, the warning line. A LocalScript.
roblox/Neighbourhood.client.lua   the "you are in Midtown" box. A LocalScript.
roblox/TaxiDriver.client.lua      drives the taxis. A LocalScript.
new-york.rbxlx                    a Roblox place with both scripts in it (made by tools/build.py)
index.html                        the web page: the map, the steps for Studio, the scripts
tools/build.py                    writes new-york.rbxlx and copies the scripts into index.html
tools/check.py                    runs the scripts in a pretend Roblox and reports mistakes
```

**The five files in `roblox/` are the real thing.** Edit those, then run
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
- **The taxis** are each a Model: an invisible box (`Chassis`) that does
  all the colliding, with the yellow body, wheels and lights welded on and
  marked `Massless` so they are only for looks. Two constraints move it. A
  `LinearVelocity` in *Plane* mode pushes it forward and sideways relative
  to the car, leaving *up* free so gravity still works and it can go up the
  bridge ramps. An `AngularVelocity` turns it about the world's Y axis and
  holds the other two axes at zero, which is why it can never flip over.
  The `VehicleSeat` is what turns W A S D into `Throttle` and `Steer`; the
  `ProximityPrompt` on it is the "press E" that sits you down.
- **Who drives the physics.** When someone sits, the server gives them
  network ownership of the chassis; from then on their own computer
  simulates the car, and `TaxiDriver` sets the two constraints every frame
  from the seat's throttle and steer. That is the standard way to make a
  Roblox car feel responsive. When they get out the server takes it back
  and sets both constraints to zero, which is the handbrake: a parked taxi
  cannot be nudged away.
- **The monster** is 25 anchored parts moved by `CFrame` every frame on
  the server. There is no animation file. A small brain at the bottom of
  `Monster.server.lua` moves a point along (towards the statue, then
  waypoints, then whichever player is in range) and turns no faster than
  `TURN_RATE`, and the body is placed around that point. The limbs are the
  interesting part: each hand or foot stays *planted* at a fixed world
  position until the body has moved more than 26 studs from where that limb
  would like to be, then it lifts and steps ahead of that spot over 0.45
  seconds. Limbs step in diagonal pairs, like a trotting dog. The elbow or
  knee is then worked out from the socket and the tip with the two-bone
  rule (both bones the same length, so the joint sits on a circle; `bend`
  says which side). The tail is six segments that each hang off the last
  and wave a little later than it.
- **What it does to the city.** `workspace:GetPartsInPart` finds anything
  inside a foot when it lands, or inside the torso every half second, from
  the folders it is allowed to break (buildings, boroughs, bridges,
  landmarks, parks). Those parts are unanchored, shoved outward and upward,
  and handed to `Debris` to vanish after 30 seconds. Because each building
  is one part, a whole skyscraper topples in one piece. Players inside a
  foot have their `Health` set to 0.
- **The head.** `BuildNewYork` names the statue's head `LibertyHead`. The
  monster unanchors it and gives it the velocity that lands a 45 degree
  throw on Wall Street: `v = sqrt(distance * gravity)`.
- **Parasites** are six anchored parts each, moved the same way, heading
  for the nearest player within 300 studs at 15 studs a second and biting
  every 0.6 seconds when they get there. They live two minutes.
- **What the client does.** `MonsterEffects` reads two attributes the server
  keeps up to date: `Phase` on `NewYorkInfo` and `Stomp` on the Monster
  model, which goes up by one per footfall, three per roar and six for the
  head. Each jump in the number becomes a camera shake that fades over half
  a second, scaled by how near the monster is. The atmosphere thickens with
  nearness; changes to `Lighting` on a client are local, so each player gets
  their own dust.
- **The client script** gets everything it needs (the shoreline, the zones,
  the grid size) from attributes the server puts in `ReplicatedStorage`, so
  it does not have its own copy of the map to keep in step.

About 6,900 parts in total, and a few seconds to build. The monster is
another 25, and up to 48 more for parasites.

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
pretend player to ten spots and prints what the neighbourhood box would say,
then sits them in a taxi, holds W, steers, and gets out, checking the car
sped up, turned the right way, and stopped. Then it fast-forwards the
monster: checks it waits its minute, surfaces, reaches the statue and takes
the head, chases a player who comes within range, drops parasites, kills a
player standing under a foot, and that the warning line appears on screen.

It cannot say whether the city *looks* right. Only Studio can.

It needs the `lupa` module: `pip install lupa`.

## Things that are only guessed at

These were decided without seeing the result in Studio, and may want changing
once someone has:

- **The Flatiron's point** should face north. If the wedge comes out pointing
  south, flip the angle in its `build` function.
- **Build time.** The terrain fill covers the whole world, including the sea.
  If the game takes too long to start, turn `BEYOND` down.
- **The monster has never been seen.** The checker proves the limbs are
  placed and the brain goes through its phases; it cannot see whether the
  elbows bend the right way (flip a limb's `bend` vector if one looks
  wrong), whether the stride looks heavy or silly (`STEP_HEIGHT` and the
  26-stud trigger in `pose`), or how the server's 20-updates-a-second
  replication looks on a 120-stud body. `HEIGHT` scales the whole thing.
- **Toppling buildings may lag.** Each stomp can unanchor up to
  `SMASH_LIMIT` parts, and a block of Midtown falling over at once is a lot
  of physics. Lower it if the game stutters when the monster is in town.
- **The taxi physics has never been driven.** The checker proves the
  numbers go to the right places; it cannot feel whether 90 studs a second
  is fun or terrifying, whether the chassis rides up the bridge ramps, or
  whether a taxi can be pushed into a river. `MAX_SPEED`, `ACCEL` and
  `TURN` at the top of `TaxiDriver` are the first things to try.
- **Water depth** is only 4 studs. If it looks wrong from a bridge, deepen
  the water fill in `buildWater`.

## Still to decide

Nothing needs Artur for this one. Everything here is free, and nothing
touches `.github/`.

- **Where do players go when the hour is up?** Alan wants each match to
  last an hour and then teleport everyone "somewhere". Two readings:
  (a) to a *different Roblox place*, a lobby, using `TeleportService`,
  which means making and publishing a second place too; (b) back to the
  spawn with the city rebuilt and the monster back in the sea, which is
  one script and no second place. Claude would start with (b): it is the
  same loop players feel, and a lobby can be added on top later.

- **Should the border be solid?** It is now (`BORDER_SOLID = true`). Alan
  asked for "a border", so that is what it does; set it to `false` to let
  players walk out into the hills. Claude would keep it solid and make the
  hills something to look at, not somewhere to get lost.
- **The border is invisible** because Alan asked for that
  (`BORDER_VISIBLE = false`). The cost is that you cannot see it coming, so
  you find it by walking into it. If that gets annoying, a thin line on the
  ground along the edge would show where it is without a wall in the sky.
