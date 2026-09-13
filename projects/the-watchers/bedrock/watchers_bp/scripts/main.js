/*
  The Watchers — the Bedrock half.

  Java does most of this with .mcfunction files. Bedrock cannot, for one
  specific reason: Bedrock has no `execute store`, so no command can get the day
  number out of the game and into a scoreboard. No day number, no timeline, and
  the timeline is the whole mod. The scripting API can simply ask.

  Nearly every call is wrapped in try/catch. The API changes between Minecraft
  versions, and one call that has moved should break one feature, not the mod.

  The rules, in one place:

    day 1-2   Watchers turn up beside you and stand there. They do not move.
              Look straight at one and it comes for you. Look away and it is
              gone when you look back.
    day 3     They come for you and for whatever you have built. From then on,
              every night, they arrive already hunting.
    day 4     Almost nothing is left alive. What is left has black eyes, comes
              for you, and its legs stretch as it runs.
    day 5     The music stops.
    day 6     More of them, every night, for good.
*/

import { world, system, BlockPermutation, EntityDamageCause } from "@minecraft/server";

const WATCHER = "watchers:watcher";
const TURNED = "watchers:turned";
const NIGHT_FROM = 13000;
const NIGHT_TO = 22800;

const MOST_AT_ONCE = 5;
const FOG_TAG = "watchersfog";

const PASSIVE = [
  "minecraft:cow", "minecraft:pig", "minecraft:sheep", "minecraft:chicken",
  "minecraft:rabbit", "minecraft:horse", "minecraft:donkey", "minecraft:mule",
  "minecraft:llama", "minecraft:fox", "minecraft:wolf", "minecraft:cat",
  "minecraft:ocelot", "minecraft:goat", "minecraft:mooshroom", "minecraft:panda",
  "minecraft:polar_bear", "minecraft:turtle", "minecraft:camel"
];

const VILLAGERS = [
  "minecraft:villager_v2", "minecraft:villager", "minecraft:wandering_trader",
  "minecraft:iron_golem", "minecraft:cat"
];

const SIGN_IDS = [
  "minecraft:standing_sign", "minecraft:oak_standing_sign",
  "minecraft:spruce_standing_sign", "minecraft:oak_sign"
];

const BOOK = [
  "It hunts at night,\nIt tasted first blood,\nand now we cannot\nreturn.",
  "It hunts as night,\nIt tasted flesh,\nand now we cannot\nreturn.",
  "It hunts at night,\nit tasted prey,\nand now we cannot\nreturn."
];

// ---------------------------------------------------------------------------
// what the mod is thinking about right now. None of this needs to survive a
// restart, and the things that do are kept in world dynamic properties below.
// ---------------------------------------------------------------------------
let lastDay = -1;
let raidDone = false;                  // has day 3 happened yet
const mind = new Map();                // watcher id -> how it is behaving
const spruceUntil = new Map();         // player id -> ticks spent in the forest
const villageUntil = new Map();        // player id -> ticks spent in a dead village
const foggy = new Set();               // players currently being fogged
const biteCooldown = new Map();
const grabbed = new Map();
let tongueCooldown = 0;
let tick = 0;

// ---------------------------------------------------------------------------
// small helpers
// ---------------------------------------------------------------------------
const day = () => { try { return world.getDay(); } catch { return 0; } };

function isNight() {
  try {
    const t = world.getTimeOfDay();
    return t >= NIGHT_FROM && t <= NIGHT_TO;
  } catch { return false; }
}

function players() {
  try {
    return world.getAllPlayers().filter(p => p.dimension.id === "minecraft:overworld");
  } catch { return []; }
}

function watchers() {
  try { return world.getDimension("overworld").getEntities({ type: WATCHER }); }
  catch { return []; }
}

const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y, a.z - b.z);
const flat = (a, b) => Math.hypot(a.x - b.x, a.z - b.z);

function say(text) { try { world.sendMessage(text); } catch {} }
function sound(p, id, v, pitch) { try { p.playSound(id, { volume: v, pitch: pitch }); } catch {} }

function groundY(dim, x, z, fromY) {
  let y = Math.min(fromY, 318);
  const stop = Math.max(-63, y - 110);
  for (; y > stop; y--) {
    let b;
    try { b = dim.getBlock({ x, y, z }); } catch { return undefined; }
    if (!b) return undefined;
    if (!b.isAir && !b.isLiquid) return y + 1;
  }
  return undefined;
}

function prop(name, fallback) {
  try {
    const v = world.getDynamicProperty(name);
    return v === undefined ? fallback : JSON.parse(v);
  } catch { return fallback; }
}

function setProp(name, value) {
  try { world.setDynamicProperty(name, JSON.stringify(value)); } catch {}
}

// ---------------------------------------------------------------------------
// Looking. Two different questions get asked about the same thing:
// "is it anywhere in front of you" and "are you staring right at it".
// ---------------------------------------------------------------------------
function inView(p, e, tightness) {
  let a, b, v;
  try {
    a = p.getHeadLocation();
    b = e.getHeadLocation();
    v = p.getViewDirection();
  } catch { return false; }
  const dx = b.x - a.x, dy = b.y - a.y, dz = b.z - a.z;
  const d = Math.hypot(dx, dy, dz);
  if (d < 1 || d > 70) return false;
  if ((dx * v.x + dy * v.y + dz * v.z) / d < tightness) return false;
  try {
    return !p.dimension.getBlockFromRay(
      a, { x: dx / d, y: dy / d, z: dz / d },
      { maxDistance: d - 1.5, includePassableBlocks: false, includeLiquidBlocks: false });
  } catch { return true; }
}

// ---------------------------------------------------------------------------
// the Watchers
// ---------------------------------------------------------------------------
function spawnWatcher(p, mode) {
  const angle = Math.random() * Math.PI * 2;
  const away = 13 + Math.random() * 14;
  const x = Math.floor(p.location.x + Math.cos(angle) * away);
  const z = Math.floor(p.location.z + Math.sin(angle) * away);
  const y = groundY(p.dimension, x, z, Math.floor(p.location.y) + 20);
  if (y === undefined) return;
  let e;
  try { e = p.dimension.spawnEntity(WATCHER, { x: x + 0.5, y, z: z + 0.5 }); }
  catch { return; }
  try { e.triggerEvent(mode === "watch" ? "watchers:start_watching" : "watchers:start_hunting"); }
  catch {}
  mind.set(e.id, { mode: mode, born: tick, seen: 0, everSeen: false });
  if (mode !== "watch") sound(p, "ambient.cave", 0.7, 0.4);
}

function goHunting(e, p) {
  const m = mind.get(e.id);
  if (!m || m.mode === "hunt") return;
  m.mode = m.mode === "watch" && day() >= 3 && isNight() ? "hunt" : "rush";
  try { e.triggerEvent("watchers:start_hunting"); } catch {}
  try { e.addEffect("speed", 200, { amplifier: 2, showParticles: false }); } catch {}
  sound(p, "mob.warden.roar", 0.9, 1.5);
  try { p.onScreenDisplay.setActionBar("§4it has seen you"); } catch {}
}

function vanish(e) {
  try { e.dimension.spawnParticle("minecraft:large_explosion", e.location); } catch {}
  mind.delete(e.id);
  try { e.remove(); } catch {}
}

/*
  The disappearing act.

  A Watcher that is only watching is allowed to exist for as long as you can
  see it. The moment it leaves your view it is taken away, so when you turn
  round it is not there. That is the whole trick: it is not hiding, it has been
  deleted, and a new one will be put somewhere else later.

  Once it is properly hunting — day three onwards, at night — it stays.
*/
function mindWatchers() {
  const ps = players();
  for (const e of watchers()) {
    let m = mind.get(e.id);
    if (!m) { m = { mode: "watch", born: tick, seen: 0, everSeen: false }; mind.set(e.id, m); }

    const near = ps.filter(p => dist(p.location, e.location) < 90);
    if (!near.length) { vanish(e); continue; }

    const looking = near.find(p => inView(p, e, 0.55));
    if (looking) { m.seen = tick; m.everSeen = true; }

    const staring = near.find(p => inView(p, e, 0.94));
    if (staring && m.mode === "watch") goHunting(e, staring);

    if (m.mode !== "hunt") {
      const gone = m.everSeen && tick - m.seen > 25;   // you looked away
      const stale = tick - m.born > 20 * 70;            // it gave up waiting
      if (gone || stale) { vanish(e); continue; }
    }

    if (m.mode === "rush" || m.mode === "hunt") {
      smash(e);
      tongue(e);
    }
  }
}

function tongue(h) {
  if (tongueCooldown > 0) return;
  let near = [];
  try {
    near = h.dimension.getPlayers({
      location: h.location, maxDistance: 14, minDistance: 4, closest: 1 });
  } catch { return; }
  if (!near.length) return;
  tongueCooldown = 120;
  const p = near[0];
  grabbed.set(p.id, 26);
  try { p.onScreenDisplay.setActionBar("§4something has hold of you"); } catch {}
  sound(p, "mob.hoglin.angry", 0.9, 0.4);
  try { h.dimension.spawnParticle("minecraft:sculk_soul_particle", h.getHeadLocation()); } catch {}
}

function reelIn() {
  const all = watchers();
  for (const [id, left] of [...grabbed]) {
    const p = players().find(q => q.id === id);
    if (!p || !all.length || left <= 0) { grabbed.delete(id); continue; }
    grabbed.set(id, left - 1);
    let h = all[0], best = 1e9;
    for (const e of all) {
      const d = dist(e.location, p.location);
      if (d < best) { best = d; h = e; }
    }
    if (best < 2.4) { grabbed.delete(id); continue; }
    const a = p.location, b = h.location;
    const d = dist(a, b);
    const to = { x: a.x + (b.x - a.x) / d * 0.45, y: a.y + (b.y - a.y) / d * 0.45,
                 z: a.z + (b.z - a.z) / d * 0.45 };
    try {
      const ahead = p.dimension.getBlock({ x: Math.floor(to.x), y: Math.floor(to.y), z: Math.floor(to.z) });
      if (!ahead || ahead.isAir || ahead.isLiquid) p.teleport(to, { keepVelocity: false });
    } catch {}
  }
}

const SOFT = /(_log$|_wood$|_planks|_leaves|glass|grass|^minecraft:dirt$|podzol|mycelium|farmland|fern|moss_block|_fence|_door$|_trapdoor|_sapling|vine|hay_block|^minecraft:web$)/;
const HARD = /(stone|deepslate|iron|copper|gold|diamond|nether|blackstone|quartz|prismarine|end_|obsidian|bedrock|brick|concrete|terracotta|basalt|tuff)/;
const isSoft = id => SOFT.test(id) && !HARD.test(id);

function smash(h) {
  let v, base;
  try { v = h.getViewDirection(); base = h.location; } catch { return; }
  for (const up of [4.4, 2.6, 0.3]) {
    const loc = { x: Math.floor(base.x + v.x * 1.1), y: Math.floor(base.y + up),
                  z: Math.floor(base.z + v.z * 1.1) };
    let b;
    try { b = h.dimension.getBlock(loc); } catch { continue; }
    if (!b || b.isAir || !isSoft(b.typeId)) continue;
    try {
      b.setPermutation(BlockPermutation.resolve("minecraft:air"));
      h.dimension.spawnParticle("minecraft:critical_hit_emitter",
        { x: loc.x + 0.5, y: loc.y + 0.5, z: loc.z + 0.5 });
    } catch {}
    return;
  }
}

// ---------------------------------------------------------------------------
// day 3: they come for you, and for what you built
// ---------------------------------------------------------------------------
function theRaid() {
  raidDone = true;
  setProp("wt_raid", true);
  say("§4§lDay 3. §r§7§oThey are not watching any more.");
  for (const p of players()) {
    for (let i = 0; i < 3; i++) spawnWatcher(p, "hunt");
    sound(p, "mob.warden.roar", 1.0, 0.6);
  }
}

// ---------------------------------------------------------------------------
// day 4: what is left of the animals
// ---------------------------------------------------------------------------
function thinTheAnimals() {
  for (const p of players()) {
    let around = [];
    try { around = p.dimension.getEntities({ location: p.location, maxDistance: 90 }); }
    catch { continue; }
    let turnedNear = around.filter(e => e.typeId === TURNED).length;
    for (const e of around) {
      if (!PASSIVE.includes(e.typeId)) continue;
      // most of them simply stop being there
      if (turnedNear >= 4 || Math.random() < 0.75) { try { e.remove(); } catch {} continue; }
      const at = e.location;
      try { e.remove(); } catch {}
      try {
        p.dimension.spawnEntity(TURNED, at);
        turnedNear++;
      } catch {}
    }
  }
}

function bite() {
  for (const p of players()) {
    let near = [];
    try { near = p.dimension.getEntities({ location: p.location, maxDistance: 3, type: TURNED }); }
    catch { continue; }
    for (const e of near) {
      const cool = biteCooldown.get(e.id) ?? 0;
      if (cool > 0) { biteCooldown.set(e.id, cool - 1); continue; }
      biteCooldown.set(e.id, 20);
      try { p.applyDamage(4, { cause: EntityDamageCause.entityAttack, damagingEntity: e }); } catch {}
    }
  }
}

// ---------------------------------------------------------------------------
// the giant spruce forest: fog, cobwebs, and more of them
// ---------------------------------------------------------------------------
const spruceCache = new Map();          // player id -> [tick, answer]

function inSpruce(p) {
  const got = spruceCache.get(p.id);
  if (got && tick - got[0] < 100) return got[1];
  let hits = 0;
  for (let i = 0; i < 22 && hits < 3; i++) {
    const x = Math.floor(p.location.x + (Math.random() * 44 - 22));
    const z = Math.floor(p.location.z + (Math.random() * 44 - 22));
    const y = groundY(p.dimension, x, z, Math.floor(p.location.y) + 20);
    if (y === undefined) continue;
    for (let k = 0; k < 12; k++) {
      let b;
      try { b = p.dimension.getBlock({ x, y: y + k, z }); } catch { break; }
      if (!b) break;
      if (b.typeId.indexOf("spruce") >= 0 || b.typeId.indexOf("podzol") >= 0) { hits++; break; }
    }
  }
  const answer = hits >= 3;
  spruceCache.set(p.id, [tick, answer]);
  return answer;
}

function fog(p, on) {
  const has = foggy.has(p.id);
  if (on === has) return;
  try {
    p.runCommand(on
      ? `fog @s push watchers:spruce_fog ${FOG_TAG}`
      : `fog @s remove ${FOG_TAG}`);
    if (on) foggy.add(p.id); else foggy.delete(p.id);
  } catch {}
}

function webTheLeaves(p) {
  for (let i = 0; i < 5; i++) {
    const x = Math.floor(p.location.x + (Math.random() * 40 - 20));
    const z = Math.floor(p.location.z + (Math.random() * 40 - 20));
    const base = Math.floor(p.location.y);
    for (let y = base + 26; y > base - 4; y--) {
      let b;
      try { b = p.dimension.getBlock({ x, y, z }); } catch { break; }
      if (!b) break;
      if (b.typeId.indexOf("leaves") < 0) continue;
      // hang a web in the air just under the leaves
      try {
        const under = p.dimension.getBlock({ x, y: y - 1, z });
        if (under && under.isAir) {
          under.setPermutation(BlockPermutation.resolve("minecraft:web"));
        }
      } catch {}
      break;
    }
  }
}

// ---------------------------------------------------------------------------
// villages, mostly empty
// ---------------------------------------------------------------------------
function villages() { return prop("wt_villages", []); }

function villageAt(loc) {
  for (const v of villages()) {
    if (Math.hypot(loc.x - v[0], loc.z - v[1]) < 70) return v;
  }
  return undefined;
}

function findVillage(p) {
  if (villageAt(p.location)) return;
  let folk = [];
  try {
    folk = p.dimension.getEntities({ location: p.location, maxDistance: 52 })
      .filter(e => VILLAGERS.includes(e.typeId));
  } catch { return; }
  if (folk.length < 2) return;

  const site = [Math.round(p.location.x), Math.round(p.location.z), Math.random() < 0.8 ? 1 : 0];
  const list = villages();
  list.push(site);
  setProp("wt_villages", list.slice(-30));
  if (!site[2]) return;                       // a few are left alone

  for (const e of folk) {
    try {
      e.dimension.spawnParticle("minecraft:basic_smoke_particle", e.location);
      e.remove();
    } catch {}
  }
  say("§8§oSomething has been through here.");
  for (let i = 0; i < 40; i++) {
    const x = Math.floor(p.location.x + (Math.random() * 60 - 30));
    const z = Math.floor(p.location.z + (Math.random() * 60 - 30));
    const y = groundY(p.dimension, x, z, Math.floor(p.location.y) + 14);
    if (y === undefined) continue;
    try {
      const b = p.dimension.getBlock({ x, y, z });
      if (b && b.isAir && Math.random() < 0.5) {
        b.setPermutation(BlockPermutation.resolve("minecraft:web"));
      }
    } catch {}
  }
}

// ---------------------------------------------------------------------------
// where the bunkers are. The first one is close enough to spawn that you will
// find it; after that they get further and further apart.
// ---------------------------------------------------------------------------
function plannedSites() {
  let sites = prop("wt_sites", null);
  if (sites) return sites;
  let spawn = { x: 0, z: 0 };
  try {
    const s = world.getDefaultSpawnLocation();
    if (s && Math.abs(s.y) < 400) spawn = s;
  } catch {}
  sites = [];
  let away = 320 + Math.random() * 520;            // the first, inside 1000
  for (let i = 0; i < 10; i++) {
    const a = Math.random() * Math.PI * 2;
    sites.push([Math.round(spawn.x + Math.cos(a) * away),
                Math.round(spawn.z + Math.sin(a) * away), 0]);
    away *= 1.75;                                   // and then rarer and rarer
  }
  setProp("wt_sites", sites);
  return sites;
}

function maybeBuild(p) {
  const sites = plannedSites();
  for (const site of sites) {
    if (site[2]) continue;
    if (Math.hypot(p.location.x - site[0], p.location.z - site[1]) > 150) continue;
    const y = groundY(p.dimension, site[0], site[1], Math.floor(p.location.y) + 40);
    if (y === undefined) return;
    try {
      const under = p.dimension.getBlock({ x: site[0], y: y - 1, z: site[1] });
      if (under && under.isLiquid) return;
      p.dimension.runCommand(
        `execute positioned ${site[0]} ${y - 1} ${site[1]} run function bunker/build`);
    } catch { return; }
    site[2] = 1;
    setProp("wt_sites", sites);
    say("§8§oYou can smell old iron on the wind.");
    const dim = p.dimension, bx = site[0], by = y, bz = site[1];
    system.runTimeout(() => plantTrees(dim, bx, by, bz), 60);
    system.runTimeout(() => writeSigns(dim, bx, by - 1, bz), 110);
    return;
  }
}

function plantTrees(dim, x, y, z) {
  for (const [dx, dz] of [[27, 15], [-23, 21], [19, -25], [-29, -17], [35, -7], [-38, 4]]) {
    const ty = groundY(dim, x + dx, z + dz, y + 22);
    if (ty === undefined) continue;
    try { dim.runCommand(`execute positioned ${x + dx} ${ty - 1} ${z + dz} run function tree/giant`); }
    catch {}
  }
}

function writeSigns(dim, x, y, z) {
  const at = [[-7, 15], [-5, 15], [-3, 15]];
  for (let i = 0; i < at.length; i++) {
    const loc = { x: x + at[i][0], y: y - 21, z: z + at[i][1] };
    for (const id of SIGN_IDS) {
      try {
        const b = dim.getBlock(loc);
        if (!b) break;
        b.setPermutation(BlockPermutation.resolve(id));
        const sign = b.getComponent("minecraft:sign");
        if (sign) sign.setText(BOOK[i]);
        break;
      } catch {}
    }
  }
}

// ---------------------------------------------------------------------------
// the day the world changes
// ---------------------------------------------------------------------------
function checkDay() {
  const d = day();
  if (d === lastDay) return;
  lastDay = d;
  const dim = world.getDimension("overworld");
  if (d === 1) say("§4§lThe Watchers§r§7§o. Nothing for two days. Then something.");
  if (d === 2) say("§4§lDay 2. §r§7§oThere is something standing at the treeline.");
  if (d === 4) say("§4§lDay 4. §r§7§oThe animals are wrong. Look at their eyes.");
  if (d === 5) say("§4§lDay 5. §r§7§oListen. There is nothing to listen to.");
  if (d === 6) say("§4§lDay 6. §r§7§oThere are more of them than there were.");
}

// ---------------------------------------------------------------------------
// the clocks
// ---------------------------------------------------------------------------
system.runInterval(() => {
  tick++;
  try {
    reelIn();
    if (tongueCooldown > 0) tongueCooldown--;
  } catch {}
}, 1);

system.runInterval(() => {
  try { mindWatchers(); } catch {}
  try { if (day() >= 4) bite(); } catch {}
}, 4);

system.runInterval(() => {
  try {
    checkDay();
    const d = day();
    const night = isNight();
    const here = watchers().length;

    if (d >= 3 && !raidDone && prop("wt_raid", false) !== true) theRaid();
    else if (d >= 3) raidDone = true;

    for (const p of players()) {
      // the forest: fog, webs, and it is worse in here
      const spruce = inSpruce(p);
      fog(p, spruce);
      if (spruce && Math.random() < 0.5) webTheLeaves(p);

      findVillage(p);
      const village = !!villageAt(p.location);

      // a minute in either place and something turns up
      const key = p.id;
      spruceUntil.set(key, spruce ? (spruceUntil.get(key) ?? 0) + 1 : 0);
      villageUntil.set(key, village ? (villageUntil.get(key) ?? 0) + 1 : 0);
      const dwelt = Math.max(spruceUntil.get(key), villageUntil.get(key));
      if (dwelt >= 60 && here < MOST_AT_ONCE) {
        spruceUntil.set(key, 0);
        villageUntil.set(key, 0);
        const how = (d >= 3 && night) ? "hunt" : "watch";
        spawnWatcher(p, how);
        if (Math.random() < 0.5) spawnWatcher(p, how);
      }

      // and otherwise, now and then, one comes to watch
      const chance = (spruce ? 0.10 : 0.02) * (d >= 6 ? 2.2 : 1) * (night ? 1.6 : 1);
      if (here < MOST_AT_ONCE && Math.random() < chance) {
        spawnWatcher(p, (d >= 3 && night) ? "hunt" : "watch");
      }

      maybeBuild(p);
      if (d >= 5) { try { p.runCommand("stopsound @s music.game"); } catch {} }
    }

    if (d >= 4) thinTheAnimals();
  } catch {}
}, 20);

const greet = () => say("§4§lThe Watchers§r§7§o is loaded. Nothing happens until day 2.");
try {
  if (world.afterEvents.worldLoad) world.afterEvents.worldLoad.subscribe(greet);
  else if (world.afterEvents.worldInitialize) world.afterEvents.worldInitialize.subscribe(greet);
} catch {}
