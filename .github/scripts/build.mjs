/* -----------------------------------------------------------------------
   Builds this repo's little website.

   Reads every folder in projects/ that has a project.json, then writes
   _site/ containing:

     _site/<slug>/...      each project, copied as-is
     _site/projects.json   the list, read by the big showcase site
     _site/index.html      this child's own page

   Run it locally with:  node .github/scripts/build.mjs
   ----------------------------------------------------------------------- */

import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

// ---- the only lines that differ between the children's repos -------------
const CHILD = 'Alan';
const REPO  = 'claude-alan';
const OWNER = 'majest';
const INK   = 'var(--blue)';
// -------------------------------------------------------------------------

const ROOT     = path.resolve(import.meta.dirname, '../..');
const PROJECTS = path.join(ROOT, 'projects');
const OUT      = path.join(ROOT, '_site');
const BASE     = `/${REPO}/`;

const problems = [];

const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const FULL   = ['January','February','March','April','May','June',
                'July','August','September','October','November','December'];

/* Read the calendar date straight off the ISO string rather than through a
   Date, so a project committed just after midnight keeps the day it was
   actually made instead of shifting a day in another timezone. */
function stamp(iso){
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(iso ?? ''));
  if (!m) return '';
  const [, y, mo, d] = m;
  const i = Number(mo) - 1;
  if (!MONTHS[i]) return '';
  return `<time class="stamp" datetime="${y}-${mo}-${d}"`
    + ` title="Made ${Number(d)} ${FULL[i]} ${y}">${Number(d)} ${MONTHS[i]} ${y}</time>`;
}

/* Date of the commit that first added a project folder. Used only for
   ordering, so if git can't tell us we just carry on without it. */
function addedOn(slug){
  try {
    const out = execFileSync('git', [
      'log', '--diff-filter=A', '--format=%aI', '--', `projects/${slug}`
    ], { cwd: ROOT, encoding: 'utf8' }).trim().split('\n').filter(Boolean);
    return out.at(-1) || null;
  } catch { return null; }
}

/* The folder name becomes part of a url, so hold it to the rule CLAUDE.md
   sets out rather than letting anything odd through into a link. */
const SLUG = /^[a-z0-9]+(-[a-z0-9]+)*$/;

function readProject(slug){
  const dir  = path.join(PROJECTS, slug);
  const meta = path.join(dir, 'project.json');

  if (!SLUG.test(slug)){
    problems.push(`projects/${slug}/ was skipped: folder names must be lowercase `
      + `letters, numbers and hyphens, like "star-map".`);
    return null;
  }

  if (!fs.existsSync(meta)){
    problems.push(`projects/${slug}/ has no project.json, so it was skipped.`);
    return null;
  }
  if (!fs.existsSync(path.join(dir, 'index.html'))){
    problems.push(`projects/${slug}/ has no index.html, so it was skipped.`);
    return null;
  }

  let json;
  try { json = JSON.parse(fs.readFileSync(meta, 'utf8')); }
  catch (e){
    problems.push(`projects/${slug}/project.json isn't valid JSON: ${e.message}`);
    return null;
  }

  if (!json.title)       problems.push(`projects/${slug}/project.json has no "title".`);
  if (!json.description) problems.push(`projects/${slug}/project.json has no "description".`);

  return {
    slug,
    title:       json.title       || slug,
    emoji:       json.emoji       || '✨',
    description: json.description || '',
    url:         `${BASE}${slug}/`,
    source:      `https://github.com/${OWNER}/${REPO}/tree/main/projects/${slug}`,
    added:       addedOn(slug),
  };
}

/* ---- collect ---------------------------------------------------------- */

const slugs = fs.existsSync(PROJECTS)
  ? fs.readdirSync(PROJECTS, { withFileTypes: true })
      .filter(e => e.isDirectory() && !e.name.startsWith('.'))
      .map(e => e.name)
  : [];

const projects = slugs
  .map(readProject)
  .filter(Boolean)
  .sort((a, b) => (b.added || '').localeCompare(a.added || '') || a.title.localeCompare(b.title));

/* ---- write ------------------------------------------------------------ */

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, '.nojekyll'), '');

for (const p of projects){
  fs.cpSync(path.join(PROJECTS, p.slug), path.join(OUT, p.slug), { recursive: true });
}

fs.writeFileSync(
  path.join(OUT, 'projects.json'),
  JSON.stringify({ child: CHILD, repo: REPO, base: BASE, projects }, null, 2) + '\n'
);

fs.writeFileSync(path.join(OUT, 'index.html'), page(projects));

/* ---- report ----------------------------------------------------------- */

console.log(`Built ${projects.length} project${projects.length === 1 ? '' : 's'} for ${CHILD}:`);
for (const p of projects) console.log(`  ${p.emoji}  ${p.title.padEnd(24)} ${p.url}`);

if (problems.length){
  console.log('\nThings to fix:');
  for (const w of problems) console.log(`  - ${w}`);
  console.log('\nSee CLAUDE.md for what a project folder needs.');
}

/* When this runs on GitHub, put the same report on the run's summary page,
   so a problem is visible without digging through the log. */
if (process.env.GITHUB_STEP_SUMMARY){
  const lines = [
    `## ${CHILD}'s site`, '',
    ...projects.map(p => `- ${p.emoji} **${p.title}** — https://${OWNER}.github.io${p.url}`),
  ];
  if (!projects.length) lines.push('_No projects published yet._');
  if (problems.length){
    lines.push('', '### Things to fix', '',
      ...problems.map(w => `- ⚠️ ${w}`), '',
      'See `CLAUDE.md` for what a project folder needs.');
  }
  fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, lines.join('\n') + '\n');
}

/* ======================================================================= */

function esc(s){
  return String(s ?? '').replace(/[&<>"]/g, c => (
    { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;' }[c]
  ));
}

function page(list){
  const tilts = [-1.4, 0.9, -0.6, 1.5, -1.1, 0.5];

  const cards = list.length ? list.map((p, i) => `
      <article class="card" style="--tilt:${tilts[i % tilts.length]}deg; --delay:${i * 70}ms">
        <div class="card-top">
          <div class="sticker" aria-hidden="true">${esc(p.emoji)}</div>
          ${stamp(p.added)}
        </div>
        <h2>${esc(p.title)}</h2>
        <p>${esc(p.description)}</p>
        <div class="actions">
          <a class="open" href="${esc(p.url)}">Open it <span>&rarr;</span></a>
          <a class="code" href="${esc(p.source)}">See the code</a>
        </div>
      </article>`).join('')
    : `
      <div class="note">
        <span class="emo">🌱</span>
        <span class="big">Nothing here yet!</span>
        ${esc(CHILD)}'s first project is on its way.
      </div>`;

  const count = !list.length ? 'nothing yet'
    : list.length === 1 ? '1 project' : `${list.length} projects`;

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>${esc(CHILD)}'s projects</title>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Things ${esc(CHILD)} has built with Claude.">
<meta name="color-scheme" content="light dark">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@9..144,400..900,0..100,0..1&family=Karla:wght@400;500;700&display=swap">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%E2%9C%A8%3C/text%3E%3C/svg%3E">
<style>
:root{
  --pink:#FF48B0; --blue:#0078BF; --green:#00A95C; --yellow:#FFC800; --orange:#FF6C2F;
  --paper:#FBF3E4; --ink:#241D18; --ink-2:#6B5D50; --ink-3:#9C8B7A;
  --rule:#DCCDB2; --card:#FFFBF2; --shadow:rgba(36,29,24,.20);
  --blend:multiply; --grain:.28; --halftone:.10; --blob-alpha:.34;
  --display:'Fraunces','Hoefler Text',Georgia,'Times New Roman',serif;
  --body:'Karla','Trebuchet MS','Helvetica Neue',Arial,sans-serif;
  --mine:${INK};
}
@media (prefers-color-scheme: dark){
  :root{
    --paper:#181A23; --ink:#F4ECDD; --ink-2:#B0A899; --ink-3:#7E786C;
    --rule:#33374A; --card:#20232E; --shadow:rgba(0,0,0,.55);
    --blend:screen; --grain:.20; --halftone:.16; --blob-alpha:.20;
  }
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;overflow-x:clip}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:var(--body); font-size:clamp(16px,.55vw + 14.5px,18px);
  line-height:1.6; overflow-x:clip; position:relative;
}
body::before{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:9;
  opacity:var(--grain); mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='240' height='240' filter='url(%23n)'/%3E%3C/svg%3E");
}
.wrap{width:min(1180px,92vw);margin-inline:auto}
a{color:inherit}
:focus-visible{outline:3px solid var(--pink);outline-offset:3px;border-radius:4px}

.masthead{position:relative;padding:clamp(3rem,7vw,5.5rem) 0 clamp(2rem,4vw,3rem);isolation:isolate}
.blobs{position:absolute;inset:-30% -15% -10%;z-index:-1;pointer-events:none;filter:blur(70px)}
.blob{position:absolute;border-radius:50%;mix-blend-mode:var(--blend);opacity:var(--blob-alpha);animation:float 22s ease-in-out infinite}
.blob.a{width:28vw;height:28vw;left:-2%;top:16%;background:var(--yellow)}
.blob.b{width:22vw;height:22vw;left:28%;top:-6%;background:var(--pink);animation-delay:-8s}
.blob.c{width:25vw;height:25vw;right:4%;top:20%;background:var(--mine);animation-delay:-14s}
@keyframes float{
  0%,100%{transform:translate3d(0,0,0) scale(1)}
  33%{transform:translate3d(2.2vw,-1.4vw,0) scale(1.07)}
  66%{transform:translate3d(-1.6vw,1.7vw,0) scale(.95)}
}
.back{
  display:block;width:max-content;margin-bottom:1.4rem;font-weight:700;font-size:.85rem;
  letter-spacing:.14em;text-transform:uppercase;color:var(--ink-2);
  text-decoration:none;border-bottom:2px solid var(--rule);padding-bottom:2px;
}
.back:hover{color:var(--ink);border-color:var(--pink)}
.masthead h1{
  margin:0;font-family:var(--display);
  font-variation-settings:'SOFT' 60,'WONK' 1,'opsz' 144;
  font-weight:900;font-size:clamp(3rem,11vw,7rem);line-height:.88;
  letter-spacing:-.025em;display:inline-block;transform:rotate(-1.5deg);
  text-shadow:.05em .04em 0 var(--mine);
}
.count{
  display:block;margin-top:1.3rem;font-size:.82rem;font-weight:700;
  letter-spacing:.18em;text-transform:uppercase;color:var(--ink-3);
}
.halftone{
  height:26px;opacity:var(--halftone);
  background-image:radial-gradient(circle at center,var(--ink) 1.6px,transparent 1.7px);
  background-size:11px 11px;
}
main{padding:clamp(2.5rem,5vw,4rem) 0}
.grid{display:grid;gap:clamp(1.4rem,2.6vw,2.2rem);grid-template-columns:repeat(auto-fill,minmax(min(272px,100%),1fr));max-width:calc(var(--cols,3) * 23rem)}
.card{
  position:relative;display:flex;flex-direction:column;
  padding:1.6rem 1.5rem 1.4rem;background:var(--card);
  border:2px solid var(--ink);border-radius:18px;
  box-shadow:6px 7px 0 var(--mine);transform:rotate(var(--tilt));
  transition:transform .28s cubic-bezier(.34,1.4,.5,1),box-shadow .28s ease;
  animation:pin .55s cubic-bezier(.2,1.3,.4,1) backwards;animation-delay:var(--delay,0ms);
}
@keyframes pin{
  from{opacity:0;transform:rotate(calc(var(--tilt) * 3)) translateY(26px) scale(.94)}
  to{opacity:1}
}
.card:hover,.card:focus-within{transform:rotate(0) translateY(-7px);box-shadow:10px 13px 0 var(--mine)}
.card-top{
  display:flex;align-items:center;justify-content:space-between;gap:.9rem;margin-bottom:1.1rem;
}
.sticker{
  width:64px;height:64px;flex:none;display:grid;place-items:center;font-size:33px;line-height:1;
  border-radius:50%;background:var(--mine);border:2px solid var(--ink);
  transform:rotate(calc(var(--tilt) * -2.2));transition:transform .3s cubic-bezier(.34,1.5,.5,1);
}
.stamp{
  flex:none;font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  white-space:nowrap;color:var(--ink-3);border:2px solid var(--rule);border-radius:999px;
  padding:.28rem .62rem;transform:rotate(calc(var(--tilt) * -1.5));
  transition:transform .3s cubic-bezier(.34,1.5,.5,1),color .2s ease,border-color .2s ease;
}
.card:hover .stamp{transform:rotate(0);color:var(--ink-2);border-color:var(--ink-3)}
.card:hover .sticker{transform:rotate(0) scale(1.09)}
.card h2{
  margin:0 0 .5rem;font-family:var(--display);
  font-variation-settings:'SOFT' 60,'WONK' 1,'opsz' 72;
  font-weight:800;font-size:1.62rem;line-height:1.05;letter-spacing:-.015em;
}
.card p{margin:0 0 1.4rem;color:var(--ink-2);font-size:.97rem;line-height:1.55;flex:1}
.actions{display:flex;align-items:center;gap:1rem;flex-wrap:wrap}
.open{
  font-weight:700;font-size:.95rem;text-decoration:none;padding:.5rem 1.05rem;
  border:2px solid var(--ink);border-radius:999px;background:var(--yellow);
  color:#241D18;box-shadow:3px 3px 0 var(--ink);
  transition:transform .15s ease,box-shadow .15s ease;
}
.open span{display:inline-block;transition:transform .22s cubic-bezier(.34,1.5,.5,1)}
.card:hover .open span{transform:translateX(4px)}
.open:active{transform:translate(3px,3px);box-shadow:0 0 0 var(--ink)}
.open::after{content:"";position:absolute;inset:0;border-radius:18px}
.code{
  position:relative;z-index:2;font-size:.82rem;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;color:var(--ink-3);text-decoration:none;
  border-bottom:2px solid var(--rule);padding-bottom:1px;
}
.code:hover{color:var(--ink);border-color:var(--pink)}
.note{
  grid-column:1 / -1;padding:2.4rem 2rem;border:3px dashed var(--rule);
  border-radius:18px;text-align:center;color:var(--ink-2);
}
.note .emo{display:block;font-size:2.2rem;margin-bottom:.7rem}
.note .big{
  display:block;font-family:var(--display);font-variation-settings:'SOFT' 80,'WONK' 1;
  font-weight:800;font-size:1.35rem;color:var(--ink);margin-bottom:.3rem;
}
footer{padding:3rem 0 4rem;color:var(--ink-3);font-size:.9rem}
footer a{color:var(--ink-2);text-decoration:none;border-bottom:2px solid var(--rule)}
footer a:hover{color:var(--ink);border-color:var(--pink)}
@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{
    animation-duration:.001ms !important;animation-iteration-count:1 !important;
    transition-duration:.001ms !important;
  }
}
</style>
</head>
<body>

<header class="masthead">
  <div class="blobs" aria-hidden="true">
    <span class="blob a"></span><span class="blob b"></span><span class="blob c"></span>
  </div>
  <div class="wrap">
    <a class="back" href="/">&larr; All the wonderful things</a>
    <h1>${esc(CHILD)}'s projects</h1>
    <span class="count">${count}</span>
  </div>
</header>

<div class="halftone" aria-hidden="true"></div>

<main class="wrap">
  <div class="grid" style="--cols:${Math.min(Math.max(list.length, 2), 4)}">${cards}
  </div>
</main>

<div class="halftone" aria-hidden="true"></div>

<footer>
  <div class="wrap">
    Made by ${esc(CHILD)} with Claude &nbsp;·&nbsp;
    <a href="https://github.com/${OWNER}/${REPO}">the code lives here</a>
  </div>
</footer>

</body>
</html>
`;
}
