# Carnivorous Plant

You are the plant. Bugs wander over because your nectar smells good, and you
have to catch them before they chew you down.

## Playing it

Choose one of four plants to start. They all catch things the way that plant
really does:

| plant | how it catches | in the game |
|-------|----------------|-------------|
| Venus Flytrap | trigger hairs inside the trap; a bug must brush two of them | small mouth, timing has to be right |
| Sundew | every arm tipped with glue; the arms curl over what sticks | bugs stick by themselves, tap in the moment after |
| Pitcher Plant | a jug of liquid with a slippery rim | big mouth, big meals, slow to empty |
| Cobra Lily | a hood of see-through windows that fool insects | hardest, worth the most |

Tap anywhere when a bug is inside your trap. Tap with nothing there and you are
shut for a moment doing nothing. Digesting takes time, and you cannot catch
anything while it happens.

Bugs sitting on you **bite**, and your health drops. Every plant can **spit
acid**, which kills a bug on the spot. Eating puts a little health back. At zero
health the plant wilts.

## Waves

Wave 1 asks for 5, and every wave after wants three more than the last. Every
fifth wave sends a **giant beetle** instead, and each one is bigger than the
last. It is far too big to swallow — only acid kills it.

Eating, acid and your special power all count towards the wave. The hunting
roots do not, on purpose: if they did, waves would clear themselves while you
sat and did nothing.

## Evolving

Digesting gives minerals. When you have enough you choose what to become, from
four picked at random, so no two games grow the same plant.

- **From the start** — wider mouth, sweeter nectar, grow larger, sharper senses
- **Past wave 5** — quicker reflexes, stronger juices, tougher leaves, deeper roots
- **Past wave 20** — your plant's own special power, hunting roots, stronger spit
- **Past wave 30** — leaf walls

Each plant has one special power only it can ever get: the flytrap's long
tongue, the sundew's grasping tentacles, the pitcher's flood of nectar, and the
cobra lily's false light.

## How it works inside

Everything is in `index.html`. There is no build step; opening the file runs it.

Two things worth knowing before changing it:

- **Plants cannot grow past `growMax()`.** Grow too big and the top of the
  plant — with your mouth on it — climbs off the top of the screen, and bugs
  fly to a spot you cannot see or reach. Taking *Grow larger* at full size
  still widens the mouth and pays more, so it is never a wasted pick.
- **Every bug is drawn in front of the plant.** They used to go behind it once
  they climbed high enough, which looked fine on a thin flytrap stem but made
  them vanish inside a pitcher plant's solid tube.

Crawling bugs walk to the bottom of the stem and climb it, which is how a real
flytrap catches ants. Leaf walls stop them on the way; flying bugs go over.
