# Alan's projects

This repo is where Alan keeps the things he builds with Claude.
Everything in here gets published to a website automatically.

Alan's page: **https://majest.github.io/claude-alan/**
All the projects: **https://majest.github.io/**

If you are Claude working in this repo, read the whole file before you make anything.
If you are Alan — hello! You can read this too. It says how everything works.

Everything needed to build a project is in this file. If this repo happens to sit
inside the family workspace, there is another `CLAUDE.md` one level up describing
how the repos fit together — useful context, but not required reading to start.

---

## First: which project?

Before changing anything, be certain which project you are in. Names overlap,
ideas are similar, and a change made in the wrong folder is worse than no
change — it quietly breaks something that was working.

If Alan says "make it bigger" or "add a sound" and it is not obvious which
project is meant, **stop and ask.** List what is there and let Alan pick:

```sh
ls projects/
```

Ask when any of these is true:

- There is more than one project it could plausibly be.
- Two projects have similar names or are about similar things.
- Alan hasn't named the project in this conversation.
- You are about to start something new and it is not clear whether it is a new
  project or a change to one that already exists.

Guessing is not being helpful. One short question costs a few seconds; editing
the wrong project costs Alan their work.

---

## Making a new project

Every project lives in its own folder inside `projects/`.
Nothing goes in the top level of the repo.

```
projects/
  snake-game/        <- one project
    index.html
    project.json
  star-map/          <- the next one
    index.html
    project.json
```

Pick a short folder name in lowercase with hyphens instead of spaces:
`snake-game`, `star-map`, `drum-machine`. No capitals, no spaces, no underscores.
The folder name becomes the web address, so `projects/star-map/` ends up at
`https://majest.github.io/claude-alan/star-map/`.

### Every project needs exactly two files

**1. `index.html` — the project itself.**

It has to start with these two lines, in this order, at the very top:

```html
<!doctype html>
<meta charset="utf-8">
```

Both matter. Without the first, browsers fall back to an old rendering mode and
the layout goes strange. Without the second, every accent, arrow, emoji and `·`
in the page turns into mojibake like `Â·`.

Then the rest of the page. The rules for what goes inside:

- **One file.** All the HTML, CSS and JavaScript go in this one file. No separate
  `style.css`, no separate `script.js`, no `src/` folder.
- **No installing.** No npm, no build step, no bundler. If someone has to run a
  command before it works, it is wrong.
- **It must work by opening the file.** Double-clicking `index.html` should run it.
  Test it that way before you finish.
- **Nothing loaded from the internet** except Google Fonts. No CDN scripts, no
  jQuery from a URL, no images hotlinked from another site. Draw pictures in code,
  or paste them in as a `data:` URI.
- **Make it work on a phone too.** Kids will open this on a tablet. Use a
  `<meta name="viewport" content="width=device-width, initial-scale=1">` and don't
  let anything spill off the side of the screen.

**2. `project.json` — how it shows up on the website.**

```json
{
  "title": "Star Map",
  "emoji": "⭐",
  "description": "A sky full of stars you can spin around. Click any star to find out its name and how far away it is."
}
```

- `title` — the proper name, with capital letters. Short.
- `emoji` — one emoji that suits it. This is the picture on its card.
- `description` — one or two sentences. This is the important one, see below.

### Writing the description

The description is what people read on the website to decide whether to click.
Write it for someone Alan's age who has never seen the project.

- Say **what it is** and **what you can do with it**. Not how it was built.
- Two sentences at most. Around 30 words.
- Plain words. No "leverages", no "utilises", no "procedurally generated
  parametric system". If a word would need explaining, use a different word.
- Present tense, talking to the reader: "you can", "click any star".

Good: *"A sky full of stars you can spin around with your finger. Tap any star to
find out its name and how far away it is."*

Not good: *"An interactive celestial visualisation leveraging a real-time WebGL
rendering pipeline over the Hipparcos catalogue."*

### A README is optional

If a project is a big one and there is more to say — how it works inside, what the
controls do — add a `README.md` in the project's folder.
Small projects don't need it.

---

## How it gets published

### Every change has to be pushed

**Finish a change, then commit it and push it to `main`. Every time.**

```sh
git add -A
git commit -m "say what changed"
git push
```

This is not tidying up for later — it is the only thing that puts the work on
the website. A change sitting on the computer uncommitted does not exist as far
as the site is concerned: Alan will look at their page, see the old version,
and think it is broken.

So don't leave finished work behind. If Alan asks for three things, push
after each one rather than saving them all up — small pushes are easier to undo
if one turns out wrong.

If a change is genuinely half-finished and shouldn't go live yet, say so out
loud rather than quietly leaving it uncommitted, so Alan knows it is waiting.

### What happens after the push

Once a change lands on the `main` branch, GitHub does this by itself:

1. It looks in `projects/` and finds every folder with a `project.json`.
2. It copies each project onto the web.
3. It builds Alan's page listing them all.
4. The big showcase site picks up the new list on its own.

It takes about a minute. Then the project is live at
`https://majest.github.io/claude-alan/<folder-name>/`.

The `.github/` folder is what does all this. **Don't edit anything in `.github/`.**
If publishing breaks, tell Artur — it isn't something to fix from inside a project.

---

## Using AI in a project

Alan might want a project that uses AI — a model that draws pictures, writes
words, or recognises what something is. That is possible, but it works
differently from everything else here, and the difference matters.

**The published page never talks to a server.** It has to keep working on a
phone, at a friend's house, on a school computer, and in ten years' time. A
page that phones home is broken for everyone except the person who built it.

So AI work happens somewhere else, ahead of time, and only the **result** comes
back into the project as an ordinary file:

- pictures a model drew once, saved as images
- words or level data generated once, saved as a `.json` file
- a small model converted to run inside the browser itself, so the page does the
  thinking on its own with no server anywhere

There is a machine at home set up to do that work. How to reach it and how to
use it are in the workspace notes on the family computer — deliberately not in
this repo, which is public. A Claude session working in the family workspace
will already have them.

If you are working from a clone somewhere else, that machine is not there. Say
so plainly rather than inventing a substitute or pointing the page at a server.

---

## Things that must never go in this repo

This repo is **public**. Anyone on the internet can read every file in it, and
everything that has ever been in it. So:

- **First names only.** No surnames, ever — not in the code, not in a comment,
  not in a description.
- No school name, no address, no town, no birthday, no age.
- No email addresses and no phone numbers.
- No photographs of Alan or of anyone he knows. Pictures drawn in code are fine.
- No passwords, no API keys, no tokens. Nothing that looks like a secret.

If a project idea needs any of those to work, it needs a different idea. Say so.

---

## A checklist before you finish

- [ ] The folder is `projects/<lowercase-hyphen-name>/`
- [ ] `index.html` starts with `<!doctype html>` and `<meta charset="utf-8">`
- [ ] Everything is in that one file, and it runs when you open it
- [ ] `project.json` has `title`, `emoji` and `description`
- [ ] The description is two plain sentences a child would understand
- [ ] Nothing from the "must never" list above is anywhere in it
- [ ] It works on a narrow phone-sized window
- [ ] It went into the project you were actually asked about
- [ ] It is committed **and pushed** — otherwise it is not on the website
