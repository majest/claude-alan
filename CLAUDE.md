# Alan's projects

This repo is where Alan keeps the things he builds with Claude. Everything in
it is published to a website automatically.

Alan's page: **https://majest.github.io/claude-alan/**
All the projects: **https://majest.github.io/**

Alan — hello. This is worth reading. It explains not just the rules but why
they are the way they are, and the "why" is the useful part.

---

## Working with Alan

**Alan is 12.** Treat him as someone building real things, because he is —
there is a 3D game in here with a chase camera.

- Explain the *why*, not just the *what*. He can follow reasoning, and knowing
  why a rule exists is what lets him decide when it matters.
- Use the real words — `function`, `array`, `canvas`, `event listener` — and
  explain a new one the first time it comes up. Don't talk around them; he'll
  need them anyway.
- Offer him the choice when there's a real trade-off. "We can do it this way,
  which is simpler, or this way, which is faster. Which do you fancy?"
- If he suggests something that won't work, say so and say why, then offer what
  will. Don't just do it and let him find out.
- Let him try things. A project that half-works and gets fixed teaches more
  than one that arrives perfect.
- Don't pad. He'll skim a wall of text, and fairly.

---

## When Artur is talking

Artur is Alan's dad.

A line beginning **`Artur:`** comes from Artur, not Alan.

- Follow it, even where it overrides what Alan asked for.
- Some things need his yes specifically: editing anything in `.github/`,
  committing a large file, and anything that costs money.
- If Alan asks for one of those, tell him it needs Artur first — and say why,
  so it isn't just a closed door.

---

## First: which project?

There are three projects in here and two of them are about carnivorous plants.
"Make the plant bigger" is genuinely ambiguous.

So before changing anything, be sure which project you're in:

```sh
ls projects/
```

Ask Alan when:

- More than one project could plausibly be meant.
- Two projects have similar names or cover similar ground.
- He hasn't named one in this conversation.
- It isn't clear whether he wants a new project or a change to an existing one.

Editing the wrong project quietly breaks something that worked, which is worse
than doing nothing. One question costs seconds.

---

## Making a new project

Each project is one self-contained folder under `projects/`:

```
projects/
  aquarium/
    index.html
    project.json
    README.md        <- optional
  venus-flytrap-project/
    index.html
    project.json
```

Folder names are lowercase with hyphens — they become the URL, so
`projects/star-map/` is served at
`https://majest.github.io/claude-alan/star-map/`. No capitals, spaces or
underscores; the build will refuse them.

### Every project needs two files

**1. `index.html`** — the project itself. It must begin:

```html
<!doctype html>
<meta charset="utf-8">
```

Without the doctype the browser falls back to a legacy rendering mode and the
layout goes subtly wrong. Without the charset it decodes the file as Latin-1,
so every arrow, accent and `·` becomes mojibake like `Â·`. Both have actually
happened here.

The rules, and the reasons:

- **One file.** All the HTML, CSS and JavaScript in `index.html`. Not because
  splitting files is bad in general — it's good practice in bigger projects —
  but because a single file always opens, always works, and can't half-load.
- **No build step.** No npm, no bundler. If someone has to run a command first,
  it's wrong for this repo.
- **It must run from the file.** Double-click `index.html` and use it. Test
  that way before you're done.
- **Nothing fetched from the internet** except Google Fonts. No CDN scripts, no
  hotlinked images. Draw things in code or inline them as `data:` URIs. Outside
  links rot, and then the project is broken years later for no good reason.
- **It has to work on a phone.** Include the viewport meta tag, and check a
  narrow window — nothing should overflow sideways.

**2. `project.json`** — what the website shows on the card:

```json
{
  "title": "The Venus Flytrap Project",
  "emoji": "📼",
  "description": "One sentence about what it is, one about what you can do."
}
```

### Writing the description

This is what decides whether anyone clicks. Write it for someone who has never
seen the project.

- What it *is* and what you can *do* — not how it was built.
- Two sentences, about 30 words.
- Plain words. If a word needs explaining, use a different one.

Good: *"A forest that grows itself. Give it a name like alder-hollow and the
same trees grow every time."*

Not good: *"An interactive canvas-based application implementing deterministic
seeded generation of arboreal scenery."*

### `README.md` is optional

Worth adding for a bigger project — how it works inside, what the controls do.
Small ones don't need it.

---

## Push every change

Finish something, then commit and push it:

```sh
git add -A
git commit -m "say what changed"
git push
```

**Every time.** The push is what publishes — there's no separate deploy step,
but nothing reaches the site until the commit is on `main`. Work sitting
uncommitted on the computer doesn't exist as far as the website is concerned,
and Alan will load his page, see the old version, and reasonably conclude it's
broken.

If he asks for three things, push after each. Small commits are easier to undo
when one turns out wrong.

If something genuinely isn't ready, say so out loud rather than quietly leaving
it uncommitted, so he knows it's waiting rather than lost.

### What the push triggers

`.github/workflows/publish.yml` runs and, in about a minute:

1. Scans `projects/` for folders containing a `project.json`.
2. Copies each project to this repo's own GitHub Pages site.
3. Generates Alan's index page and a `projects.json` listing.
4. The main showcase reads that listing and shows the new project.

Each repo publishes **itself**, using its own credentials, so nothing here has
write access to anything else. That's deliberate — it means there is no token
anywhere in this repo to leak.

**Don't edit `.github/`.** If publishing breaks, that's one for Artur.

---

## Using AI in a project

Alan might want a project that uses AI — a model that generates images, writes
text, or classifies something. That's possible, and it works differently from
everything else here.

**The published page must never call a server.** Three reasons, and any one of
them is enough:

- The page runs on other people's devices, at school and at friends' houses. A
  page that depends on a machine at home is broken for everyone but Alan.
- The site is served over HTTPS, and browsers block HTTPS pages from calling
  plain HTTP addresses.
- Home addresses like `192.168.x.x` don't exist outside the house anyway.

So the model runs **ahead of time**, elsewhere, and only its output is
committed here:

- images generated once and saved as files
- text, dialogue or level data generated once and saved as JSON
- a small model converted to run *inside the browser* with ONNX Runtime Web or
  TensorFlow.js — the page does the inference itself, no server involved

That last one is the interesting option and the honest way for a page to "use
AI". It keeps working on a phone, offline, and in ten years.

There's a machine at home set up for this work. How to reach it and how to use
it are in the family notes on Artur's computer — **deliberately not in this
repo, which is public.** A session working in the family workspace will already
have them.

If those notes aren't available, that machine isn't either. Say so plainly
rather than inventing a substitute.

---

## Multiplayer games

For a game two people play at once on different computers, the two browsers
need somewhere to exchange moves. A static page can't do that alone.

There's a small service set up for exactly this. The mental model: **a shared
notepad on the internet, organised into rooms.** One player writes a move, the
other reads it. Everything is deleted automatically after an hour — nothing is
stored long-term.

The page **polls** it: every second or so it asks "anything new?" and redraws
if so. That's simple, robust, and plenty for turn-based games — noughts and
crosses, battleships, a quiz buzzer, drawing together, a shared lobby.

It is *not* right for fast action games where players move continuously. That
needs a persistent connection (WebSockets), which is a bigger piece of work —
worth doing if Alan wants it, but as its own project, not bolted on.

Two rules:

- Using the service that already exists is fine any time.
- **Creating or changing anything out there needs `Artur:`**, because it costs
  money and runs under his account.

The address and how to call it are in the family notes, not in this repo.

**Anything sent through it is readable by anyone** who knows the room name.
It's for game moves. Never names, never anything private.

---

## Things that must never go in this repo

This repo is public, and so is every commit ever made to it. Deleting a file
later does not remove it from history.

- **First names only.** No surnames, anywhere — not in code, comments or
  descriptions.
- No school, address, town, birthday or age.
- No email addresses, no phone numbers.
- No photographs of Alan or anyone he knows. Drawn or generated images are fine.
- No passwords, API keys or tokens. Nothing that looks like a secret.
- Nothing about the machines at home — no addresses, usernames or setup details.

If an idea needs any of those, it needs a different idea. Say so.

---

## Checklist before you finish

- [ ] Folder is `projects/<lowercase-hyphen-name>/`
- [ ] `index.html` starts with `<!doctype html>` and `<meta charset="utf-8">`
- [ ] Everything is in that one file, and it runs when opened directly
- [ ] `project.json` has `title`, `emoji` and `description`
- [ ] Description is two plain sentences, no jargon
- [ ] Nothing from the "must never" list is anywhere in it
- [ ] It works in a narrow, phone-sized window
- [ ] It went into the project Alan actually asked about
- [ ] Committed **and pushed** — or Alan has been told it's waiting
