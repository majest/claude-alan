# Aquarium

A game about looking after a fish tank. Mould grows on the glass and dirt
floats in the water, and cleaning it up is how you earn money.

## Playing it

Along the bottom of the room there are three things you can pick up. Tap one to
pick it up, tap it again to put it back.

- **The net** leans on the right of the tank. Sweep it through the water to
  scoop out dirt.
- **The cloth** sits on the floor on the left. Rub it over the green mould on
  the glass. You only get paid once a whole patch is gone.
- **The tub of food** is next to the cloth. Hold it over the tank and shake it
  side to side to sprinkle seaweed flakes in. Everything hungry swims over.
  Flakes nobody eats sink, and some of them turn into dirt.

Tap any creature to see how it is doing. If its health says **Ill** in red,
tap and hold it, drag it out of the tank, and hold it over the white box with
the green plus until the bar turns green. Then let go over the water.

## What a patch of mould is worth

Measured by how much of the glass it covers, so it works the same in every tank:

| patch | pays |
|-------|------|
| small | $1–5 |
| middling | $6–10 |
| big | $10–20 |

People come to watch the tank, and everybody watching pays up every 20 seconds.

## The shop

- **Tanks** — five of them, from a 2 m × 1 m box up to a 10 m × 15 m cylinder.
  Buy them in order, then equip the one you want.
- **Fish** — goldfish, clownfish, a European lobster, an octopus and a lionfish.
  You can keep as many kinds at once as you like. Clownfish need the second tank.
- **Upgrades** — a bigger cloth and net, a filter, better pay, more seats,
  posters, and people who clean for you. Each one goes up in levels.

## How it works inside

Everything is in `index.html`. There is no build step; opening the file runs it.

Two ideas run through the code:

- **Real things are measured in metres.** Coral, caves, rocks and the tanks
  themselves are given real sizes, and `PPM` (dots per metre) turns them into
  dots. That is why everything looks smaller in a bigger tank.
- **Things you play with are measured against the tank.** Mould patches, bits
  of dirt, and the cloth and net are all a share of the tank's width. If they
  were fixed sizes, the cloth would be wider than a whole patch of mould in the
  big tanks and cleaning them would be trivial.

`setGeometry()` works out the shape of whichever tank is equipped, and every
drawing function reads from it, so adding a tank means adding an entry to
`TANKS` and nothing else.
