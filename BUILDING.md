# How projects work here

The rules for building anything in this repo. They are the same in Alan's repo
and Adam's — only the way you explain them differs, and that is in `CLAUDE.md`.

Written plainly so either of them can read it. When talking to a child, use
their own level rather than reading this out.

---

## First: which project?

Before changing anything, be sure which project you are in. Names overlap and
ideas are similar, so "make it bigger" is often ambiguous.

```sh
ls projects/
```

Ask when any of these is true:

- More than one project could plausibly be meant.
- Two projects have similar names or cover similar ground.
- The child hasn't named one in this conversation.
- It isn't clear whether they want a new project or a change to an existing one.

Editing the wrong project quietly breaks something that worked, which is worse
than doing nothing. One question costs seconds.

---

## Where a project lives

One folder per project, inside `projects/`:

```
projects/
  alien-clash/
    index.html
    project.json
    README.md        <- optional
  snake-game/
    index.html
    project.json
```

Folder names are lowercase letters, numbers and hyphens. No capitals, no
spaces, no underscores — the build refuses them. The folder name becomes the
web address, so `projects/star-map/` is served at
`https://majest.github.io/<this-repo>/star-map/`.

## The two files every project needs

### 1. `index.html` — the project itself

It must begin with these two lines:

```html
<!doctype html>
<meta charset="utf-8">
```

Without the doctype the browser falls back to a legacy rendering mode and the
layout goes subtly wrong. Without the charset it decodes the file as Latin-1,
so every arrow, accent and `·` turns into mojibake like `Â·`. Both have
actually happened here.

Then the rest of the page:

- **One file.** All the HTML, CSS and JavaScript in `index.html`. Not because
  splitting files is bad in general — it is good practice in bigger projects —
  but because a single file always opens, always works, and cannot half-load.
- **No build step.** No npm, no bundler. If someone has to run a command before
  it works, it is wrong for this repo.
- **It must run from the file.** Double-click `index.html` and use it. Test
  that way before finishing.
- **Nothing fetched from the internet** except Google Fonts, and the pinned AI
  libraries and models listed in `AI-TOOLBOX.md`. No other CDN scripts, no
  hotlinked images. Draw things in code or inline them as `data:` URIs. Outside
  links rot, and the project is broken years later for no good reason.
- **It has to work on a phone.** Include the viewport meta tag and check a
  narrow window — nothing should spill off the side.

Generated pictures, sounds and data files live in the project folder alongside
`index.html`. The one-file rule is about code, not assets.

### 2. `project.json` — what the website shows

```json
{
  "title": "Alien Clash",
  "emoji": "👽",
  "description": "A card game where every alien is invented the second you flip it. Pick a power, the biggest number wins the pile."
}
```

**The description is the important field.** It is what someone reads before
deciding to click.

- Say what it *is* and what you can *do* with it — not how it was built.
- Two sentences, around 30 words.
- Plain words. If a word would need explaining, use a different word.

Good: *"A forest that grows itself. Give it a name like alder-hollow and the
same trees grow every time."*

Not good: *"An interactive canvas-based application implementing deterministic
seeded generation of arboreal scenery."*

### `README.md` is optional

Worth adding for a bigger project — how it works inside, what the controls do.
Small ones do not need one.

---

## Push every change

Finish something, then commit and push it:

```sh
git add -A
git commit -m "say what changed"
git push
```

**Every time.** The push is what publishes. There is no separate deploy step,
but nothing reaches the website until the commit is on `main`. Work sitting
uncommitted is invisible to the site, and the child will load their page, see
the old version, and reasonably conclude it is broken.

If they ask for three things, push after each one. Small commits are easier to
undo when one turns out wrong.

If something genuinely is not ready, say so out loud rather than quietly
leaving it uncommitted, so they know it is waiting rather than lost.

### What the push triggers

`.github/workflows/publish.yml` runs and, in about a minute:

1. Scans `projects/` for folders containing a `project.json`.
2. Copies each project to this repo's own GitHub Pages site.
3. Generates the child's index page and a `projects.json` listing.
4. The main showcase reads that listing and shows the new project.

Each repo publishes **itself**, with its own credentials, so nothing here has
write access to anything else. That is deliberate: there is no token in this
repo to leak.

**Don't edit `.github/`.** If publishing breaks, that is one for Artur.

---

## Using AI

**`AI-TOOLBOX.md` is the menu.** Ten capabilities that run in the player's own
browser — speech in and out, hand and gesture and body and face tracking,
cutting a person out of the camera, and heavier text and image models. Each
entry has a measured size, a measured load time, and code to copy.

**Look there first.** It covers most of what gets asked for, needs no server,
no key and no cost, and works for everyone the child shows it to.

There is also a machine at home with a graphics card, for things the browser
cannot do well — proper artwork, 3D models, character voices, music, and text
that has to read well. It works differently:

- It makes **files, ahead of time.** Those files get committed here and the
  page loads them like any other asset.
- **The published page never calls it.** That machine has no public address, so
  a page that depended on it would be broken for everyone except the family.
- How to reach it is in the workspace notes on Artur's computer, deliberately
  not in this repo. If those notes are not available, neither is the machine —
  say so rather than inventing a substitute.

---

## Multiplayer

For a game two people play at once on different computers, the browsers need
somewhere to swap moves. There is a small service for exactly that:

```
https://pr27r9l9jc.execute-api.eu-west-2.amazonaws.com
```

A **room** is a name two players agree on. One posts a move, the other reads
what is new. Everything is deleted after an hour.

```js
const ROOMS = "https://pr27r9l9jc.execute-api.eu-west-2.amazonaws.com";

// send a move
await fetch(ROOMS, {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ room: "alan-v-adam", move: { square: 4, mark: "x" } }),
});

// read what is new; the reply is { moves: [...], now: N }
// keep that `now` and send it back as the next `since`
const res = await fetch(ROOMS, {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ room: "alan-v-adam", since }),
});
```

Limits: room names are lowercase letters, numbers and hyphens up to 40
characters; one move must be under 4 KB; a read returns at most 200 moves.

**Always stop polling when the game ends or the page is hidden** — a forgotten
loop runs all night:

```js
addEventListener("pagehide", stop);
```

Good for turn-based play: noughts and crosses, battleships, a quiz buzzer,
drawing together. Not for continuous movement — that needs a persistent
connection, which is a separate and much larger build.

**Anything sent through it is readable by anyone who knows the room name.**
Game moves only. Never names, never anything private.

---

## Things that must never go in this repo

This repo is public, and so is every commit ever made to it. Deleting a file
later does not remove it from history.

- **First names only.** No surnames, anywhere — not in code, comments or
  descriptions.
- No school, address, town, birthday or age.
- No email addresses, no phone numbers.
- No photographs of the children or anyone they know. Drawn or generated
  images are fine.
- No passwords, API keys or tokens. Nothing that looks like a secret.
- Nothing about the machines at home — no addresses, usernames or setup
  details.

If an idea needs any of those, it needs a different idea. Say so.

---

## Checklist before finishing

- [ ] It went into the project the child actually asked about
- [ ] Folder is `projects/<lowercase-hyphen-name>/`
- [ ] `index.html` starts with `<!doctype html>` and `<meta charset="utf-8">`
- [ ] All the code is in that one file, and it runs when opened directly
- [ ] `project.json` has `title`, `emoji` and `description`
- [ ] The description is two plain sentences
- [ ] It works in a narrow, phone-sized window
- [ ] Nothing from the "must never" list is anywhere in it
- [ ] Committed **and pushed** — or the child has been told it is waiting
