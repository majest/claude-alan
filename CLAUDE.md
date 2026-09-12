# Alan's projects

This is where Alan keeps the things he builds with Claude. Everything here is
published to a website automatically.

Alan's page: **https://majest.github.io/claude-alan/**
Everyone's page: **https://majest.github.io/**

Alan — hello. This is worth reading. It says how to work with you; the rules
themselves are next door in `BUILDING.md`.

---

## This file is only about Alan

**The rules for building are not in this repo.** They live one folder up, in
the family workspace on Artur's computer, because they are the same for
Alan and Adam and there should only be one copy:

- **`BUILDING.md`** — folders, the two files a project needs, pushing, and what
  must never go in here. Read it before making anything.
- **`AI-TOOLBOX.md`** — every AI capability available, with code to copy.

A session working on Artur's computer can read both. This file is what differs, and
it is about one thing: **Alan is 12, and that changes how you work with him,
not what the rules are.**

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

## Where everything else is

**In this repo:**

| | |
| --- | --- |
| `CLAUDE.md` | this file — how to work with Alan |
| `README.md` | what is in this repo |
| `projects/<name>/README.md` | optional, per project |

**One folder up**, in the family workspace on Artur's computer and not
published:

| | |
| --- | --- |
| `BUILDING.md` | how to make a project — **the rules** |
| `AI-TOOLBOX.md` | every AI capability, with code |
| `CLAUDE.md` | how the repos, the website, the machine at home and the cloud fit together |

Those are found automatically when working on Artur's computer.

🔴 **If they are not there, this repo has been cloned somewhere else, and you do
not have the rules.** Do not guess them and do not invent them. Say plainly
that the workspace files are missing and ask for them.
