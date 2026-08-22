# Alan's projects

This repo is where Alan keeps the things he builds with Claude.
Everything in here gets published to a website automatically.

Alan's page: **https://majest.github.io/claude-alan/**
All the projects: **https://majest.github.io/**

If you are Claude working in this repo, read the whole file before you make anything.
If you are Alan — hello! You can read this too. It says how everything works.

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

It has to start with this line, on its own, at the very top:

```html
<!doctype html>
```

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

Alan doesn't have to do anything. When a change lands on the `main` branch,
GitHub does this by itself:

1. It looks in `projects/` and finds every folder with a `project.json`.
2. It copies each project onto the web.
3. It builds Alan's page listing them all.
4. The big showcase site picks up the new list on its own.

It takes about a minute. Then the project is live at
`https://majest.github.io/claude-alan/<folder-name>/`.

The `.github/` folder is what does all this. **Don't edit anything in `.github/`.**
If publishing breaks, tell Artur — it isn't something to fix from inside a project.

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
- [ ] `index.html` starts with `<!doctype html>`
- [ ] Everything is in that one file, and it runs when you open it
- [ ] `project.json` has `title`, `emoji` and `description`
- [ ] The description is two plain sentences a child would understand
- [ ] Nothing from the "must never" list above is anywhere in it
- [ ] It works on a narrow phone-sized window
