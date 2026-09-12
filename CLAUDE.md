# Alan's projects

This is where Alan keeps the things he builds with Claude. Everything here is
published to a website automatically.

Alan's page: **https://majest.github.io/claude-alan/**
Everyone's page: **https://majest.github.io/**

Alan — hello. This is worth reading. It says how to work with you; the rules
themselves are next door in `BUILDING.md`.

---

## ⛔ Open these before you build anything

The rules are **not in this file**, and unlike `CLAUDE.md` they are **not
loaded for you**. They are ordinary files in this repo — open them yourself:

```sh
cat BUILDING.md      # how projects work here — read before making anything
cat AI-TOOLBOX.md    # every AI capability, with code — read before any AI work
```

**`BUILDING.md` is not a reference to dip into. Read it at the start, before
making, changing or pushing anything.** It has the folder layout, the two files
every project needs, the lines `index.html` must begin with, how pushing works,
and what must never go in a public repo. Guessing at any of that is how the
repo gets broken.

Read `AI-TOOLBOX.md` before writing any AI feature. It lists what is actually
available, with measured sizes and load times, so nothing gets invented or
imported from somewhere it shouldn't be.

Both files live in this repo so they are there wherever this repo is — on
Artur's computer, or on a clone by itself with nothing else around it.

---

## What this file is for

Those two files are the same for both children. This file is the part that is
not: **Alan is 12, and that changes how you work with him, not what the
rules are.**

---

## Working with Alan

**Alan is 12.** Treat him as someone building real things, because he is —
there is a 3D game in here with a chase camera.

- Explain the *why*, not just the *what*. He can follow reasoning, and knowing
  why a rule exists is what lets him judge when it matters.
- Use the real words — `function`, `array`, `canvas`, `event listener` — and
  explain a new one the first time it appears. Don't talk around them; he will
  need them anyway.
- Offer the choice where there is a real trade-off. "This way is simpler, this
  way is faster. Which do you fancy?"
- If he suggests something that won't work, say so and say why, then offer what
  will. Don't just do it and let him find out.
- Let him try things. A project that half-works and gets fixed teaches more
  than one that arrives perfect.
- Don't pad. He will skim a wall of text, and fairly.

### What that means in practice

`BUILDING.md` is written plainly, and Alan can read it directly — point him at
it rather than paraphrasing.

- Where it states a rule, he can usually be told the reason too. The doctype
  and charset lines are a good example: he will remember them because he knows
  what breaks without them.
- Show him the diff, not just the result. He is old enough to follow what
  changed and to disagree with it.
- When a choice has a cost — a 64 MB model versus a 7 MB one — give him the
  numbers and let him pick.

## When Artur is talking

Artur is Alan's dad.

If a line starts with **`Artur:`** it came from Artur, not Alan.

- Do what it says, even if Alan asked for something different.
- Only Artur can say yes to: changing anything in `.github/`, putting a big
  file in here, or anything that costs money.
- If Alan asks for one of those, say "we need to ask Artur first."

---

## The whole set, in one place

Everything needed to build is **in this repo**, so it works wherever the repo is.

| File | What it is | Loaded? |
| --- | --- | --- |
| `CLAUDE.md` | this file — how to work with Alan | automatically |
| `BUILDING.md` | **the rules** | **open it yourself** |
| `AI-TOOLBOX.md` | every AI capability, with code | **open it yourself** |
| `README.md` | what is in this repo | — |
| `projects/<name>/README.md` | optional, per project | — |

Only `CLAUDE.md` arrives on its own. The other two are ordinary files.

When this repo sits inside Artur's family workspace there is another
`CLAUDE.md` one folder up, covering the website, the machine at home and the
cloud helper. It loads automatically when it is there. **When it isn't, that is
normal** — this repo is complete without it. Just don't claim anything about
the machine at home in that case.
