/*
  Scopophobia — the Bedrock half.

  Java does all of this with .mcfunction files. Bedrock cannot, for one
  specific reason: Bedrock has no `execute store`, so there is no way to get
  the day number out of the game and into a scoreboard. Without that there is
  no timeline, and the timeline is the whole mod.

  So Bedrock uses the scripting API instead, which is plain JavaScript running
  inside Minecraft. It can ask the world what day it is, which is all we needed
  in the first place — and once you are in JavaScript, everything else is
  easier to write and easier to read.

  Nearly every call here is wrapped in try/catch. The scripting API changes
  between Minecraft versions, and one call that does not exist any more should
  break one feature, not the whole mod.
*/

import { world, system, BlockPermutation, EntityDamageCause } from "@minecraft/server";

const HUNTER = "scopophobia:hunter";
const NIGHT_FROM = 13000;
const NIGHT_TO = 22800;

// animals that turn on day 3
const PASSIVE = [
  "minecraft:cow", "minecraft:pig", "minecraft:sheep", "minecraft:chicken",
  "minecraft:rabbit", "minecraft:horse", "minecraft:donkey", "minecraft:mule",
  "minecraft:llama", "minecraft:villager_v2", "minecraft:villager",
  "minecraft:wandering_trader", "minecraft:fox", "minecraft:wolf",
  "minecraft:cat", "minecraft:ocelot", "minecraft:goat", "minecraft:mooshroom",
  "minecraft:panda", "minecraft:polar_bear", "minecraft:turtle", "minecraft:camel"
];

const SWARM = [
  "minecraft:zombie", "minecraft:skeleton", "minecraft:spider",
  "minecraft:creeper", "minecraft:husk", "minecraft:zombie"
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

let lastDay = -1;
let tongueCooldown = 0;
let biteCooldown = new Map();    // entity id -> ticks left
const grabbed = new Map();       // player id -> ticks left

// ---------------------------------------------------------------------------
// small helpers
// ---------------------------------------------------------------------------
function day() {
  try { return world.getDay(); } catch { return 0; }
}

function isNight() {
  try {
    const t = world.getTimeOfDay();
    return t >= NIGHT_FROM && t <= NIGHT_TO;
  } catch { return false; }
}

function overworlders() {
  try {
    return world.getAllPlayers().filter(p => p.dimension.id === "minecraft:overworld");
  } catch { return []; }
}

function theHunter() {
  try {
    const found = world.getDimension("overworld").getEntities({ type: HUNTER });
    return found.length ? found[0] : undefined;
  } catch { return undefined; }
}

function dist(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y, a.z - b.z);
}

/** Walk down from `fromY` until something solid is underfoot. */
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

function say(text) {
  try { world.sendMessage(text); } catch {}
}

function sound(player, id, volume, pitch) {
  try { player.playSound(id, { volume: volume, pitch: pitch }); } catch {}
}

// ---------------------------------------------------------------------------
// where the bunkers already are, remembered between one play and the next
// ---------------------------------------------------------------------------
function sites() {
  try { return JSON.parse(world.getDynamicProperty("sc_bunkers") ?? "[]"); }
  catch { return []; }
}

function rememberSite(x, y, z) {
  try {
    const list = sites();
    list.push([Math.round(x), Math.round(y), Math.round(z)]);
    world.setDynamicProperty("sc_bunkers", JSON.stringify(list.slice(-40)));
  } catch {}
}

function nearASite(loc, range) {
  for (const [x, y, z] of sites()) {
    if (Math.hypot(loc.x - x, loc.z - z) < range) return true;
  }
  return false;
}

// ---------------------------------------------------------------------------
// the creature
// ---------------------------------------------------------------------------
function spawnHunter() {
  const players = overworlders();
  if (!players.length) return;
  const p = players[Math.floor(Math.random() * players.length)];
  const angle = Math.random() * Math.PI * 2;
  const away = 38 + Math.random() * 16;
  const x = Math.floor(p.location.x + Math.cos(angle) * away);
  const z = Math.floor(p.location.z + Math.sin(angle) * away);
  const y = groundY(p.dimension, x, z, Math.floor(p.location.y) + 30);
  if (y === undefined) return;
  try {
    p.dimension.spawnEntity(HUNTER, { x: x + 0.5, y: y, z: z + 0.5 });
  } catch { return; }
  for (const q of players) sound(q, "ambient.cave", 0.8, 0.5);
}

function hunterLeaves(h) {
  try {
    h.dimension.spawnParticle("minecraft:large_explosion", h.location);
  } catch {}
  try { h.remove(); } catch {}
}

/** Does any player have it dead in their sights, with nothing in the way? */
function stareCheck(h) {
  for (const p of overworlders()) {
    let a, b, v;
    try {
      a = p.getHeadLocation();
      b = h.getHeadLocation();
      v = p.getViewDirection();
    } catch { continue; }
    const dx = b.x - a.x, dy = b.y - a.y, dz = b.z - a.z;
    const d = Math.hypot(dx, dy, dz);
    if (d < 2 || d > 48) continue;
    // how closely their line of sight matches the way to the creature:
    // 1 is straight at it, 0 is side on
    const aim = (dx * v.x + dy * v.y + dz * v.z) / d;
    if (aim < 0.96) continue;
    let blocked = false;
    try {
      blocked = !!p.dimension.getBlockFromRay(
        a, { x: dx / d, y: dy / d, z: dz / d },
        { maxDistance: d - 1.2, includePassableBlocks: false, includeLiquidBlocks: false }
      );
    } catch {}
    if (blocked) continue;
    seenBy(h, p);
  }
}

function seenBy(h, p) {
  try { h.addEffect("speed", 100, { amplifier: 2, showParticles: false }); } catch {}
  sound(p, "mob.warden.roar", 0.8, 1.7);
  try { p.onScreenDisplay.setActionBar("§4it has seen you"); } catch {}
}

function tongue(h) {
  if (tongueCooldown > 0) return;
  let near = [];
  try {
    near = h.dimension.getPlayers({
      location: h.location, maxDistance: 12, minDistance: 3, closest: 1
    });
  } catch { return; }
  if (!near.length) return;
  tongueCooldown = 120;
  const p = near[0];
  grabbed.set(p.id, 24);
  try { p.onScreenDisplay.setActionBar("§4something has hold of you"); } catch {}
  sound(p, "mob.hoglin.angry", 0.9, 0.4);
  try { h.dimension.spawnParticle("minecraft:sculk_soul_particle", h.getHeadLocation()); } catch {}
}

function reelIn(h) {
  for (const [id, left] of [...grabbed]) {
    const p = overworlders().find(q => q.id === id);
    if (!p || !h || left <= 0) { grabbed.delete(id); continue; }
    grabbed.set(id, left - 1);
    const a = p.location, b = h.location;
    const dx = b.x - a.x, dy = b.y - a.y, dz = b.z - a.z;
    const d = Math.hypot(dx, dy, dz);
    if (d < 1.7) { grabbed.delete(id); continue; }
    const step = 0.42;
    const to = { x: a.x + (dx / d) * step, y: a.y + (dy / d) * step, z: a.z + (dz / d) * step };
    let clear = true;
    try {
      const b2 = p.dimension.getBlock({ x: Math.floor(to.x), y: Math.floor(to.y), z: Math.floor(to.z) });
      clear = !b2 || b2.isAir || b2.isLiquid;
    } catch {}
    if (!clear) continue;
    try { p.teleport(to, { keepVelocity: false }); } catch {}
  }
}

/*
  Wood, glass, leaves, grass and dirt, and nothing else.

  The entity has a minecraft:break_blocks component listing all of those, and
  that is what should do the work. This is the belt as well as the braces: if
  that component is not doing anything on your version, this still smashes a
  way through. Stone, iron and obsidian are not on the list, so a stone room is
  still worth building.
*/
const SOFT = /(_log$|_wood$|_planks|_leaves|glass|grass|^minecraft:dirt$|podzol|mycelium|farmland|fern|moss_block|_fence|_door$|_trapdoor|_sapling|vine|hay_block)/;
const HARD = /(stone|deepslate|iron|copper|gold|diamond|nether|blackstone|quartz|prismarine|end_|obsidian|bedrock|brick|concrete|terracotta|basalt|tuff)/;

function isSoft(id) {
  return SOFT.test(id) && !HARD.test(id);
}

function smash(h) {
  let v, base;
  try { v = h.getViewDirection(); base = h.location; } catch { return; }
  for (const up of [1.3, 0.2]) {
    const loc = {
      x: Math.floor(base.x + v.x * 0.9),
      y: Math.floor(base.y + up),
      z: Math.floor(base.z + v.z * 0.9)
    };
    let b;
    try { b = h.dimension.getBlock(loc); } catch { continue; }
    if (!b || b.isAir || !isSoft(b.typeId)) continue;
    try {
      b.setPermutation(BlockPermutation.resolve("minecraft:air"));
      h.dimension.spawnParticle("minecraft:critical_hit_emitter", {
        x: loc.x + 0.5, y: loc.y + 0.5, z: loc.z + 0.5
      });
    } catch {}
    return;
  }
}

// ---------------------------------------------------------------------------
// day 3: the animals turn
// ---------------------------------------------------------------------------
function turnSome() {
  for (const p of overworlders()) {
    let around = [];
    try {
      around = p.dimension.getEntities({ location: p.location, maxDistance: 44 });
    } catch { continue; }
    let turned = 0;
    for (const e of around) {
      if (turned >= 4) break;
      try {
        if (!PASSIVE.includes(e.typeId) || e.hasTag("sc_turned")) continue;
        e.addTag("sc_turned");
        e.addEffect("speed", 999999, { amplifier: 0, showParticles: false });
        turned++;
      } catch {}
    }
  }
}

function chaseTurned() {
  for (const p of overworlders()) {
    let around = [];
    try {
      around = p.dimension.getEntities({ location: p.location, maxDistance: 28, tags: ["sc_turned"] });
    } catch { continue; }
    for (const e of around) {
      try {
        const a = e.location, b = p.location;
        const dx = b.x - a.x, dz = b.z - a.z;
        const flat = Math.hypot(dx, dz);
        if (flat > 0.6) {
          const step = 0.34;
          const to = { x: a.x + (dx / flat) * step, y: a.y, z: a.z + (dz / flat) * step };
          const ahead = e.dimension.getBlock({ x: Math.floor(to.x), y: Math.floor(to.y + 0.2), z: Math.floor(to.z) });
          if (!ahead || ahead.isAir || ahead.isLiquid) e.teleport(to);
        }
        const cool = biteCooldown.get(e.id) ?? 0;
        if (dist(a, b) < 1.9 && cool <= 0) {
          biteCooldown.set(e.id, 20);
          p.applyDamage(3, { cause: EntityDamageCause.entityAttack, damagingEntity: e });
        }
        // a wrongness you can see without a texture pack
        if (Math.random() < 0.08) {
          e.dimension.spawnParticle("minecraft:basic_smoke_particle", {
            x: a.x, y: a.y + 1.1, z: a.z
          });
        }
      } catch {}
    }
  }
  for (const [id, left] of [...biteCooldown]) {
    if (left <= 4) biteCooldown.delete(id); else biteCooldown.set(id, left - 4);
  }
}

// ---------------------------------------------------------------------------
// day 5 and day 6
// ---------------------------------------------------------------------------
function goQuiet() {
  for (const p of overworlders()) {
    try { p.runCommand("stopsound @s music.game"); } catch {}
  }
}

function cull() {
  for (const p of overworlders()) {
    let around = [];
    try { around = p.dimension.getEntities({ location: p.location, maxDistance: 110, minDistance: 48 }); }
    catch { continue; }
    const fodder = around.filter(e => e.typeId !== HUNTER
      && e.typeId !== "minecraft:player" && !e.hasTag("sc_turned"));
    for (let i = 0; i < 2 && fodder.length; i++) {
      const e = fodder.splice(Math.floor(Math.random() * fodder.length), 1)[0];
      try { e.remove(); } catch {}
    }
  }
}

function swarm() {
  const players = overworlders();
  if (!players.length) return;
  const p = players[Math.floor(Math.random() * players.length)];
  let around = [];
  try { around = p.dimension.getEntities({ location: p.location, maxDistance: 55 }); } catch { return; }
  if (around.length > 24) return;
  const angle = Math.random() * Math.PI * 2;
  const away = 20 + Math.random() * 22;
  const x = Math.floor(p.location.x + Math.cos(angle) * away);
  const z = Math.floor(p.location.z + Math.sin(angle) * away);
  const y = groundY(p.dimension, x, z, Math.floor(p.location.y) + 24);
  if (y === undefined) return;
  const what = SWARM[Math.floor(Math.random() * SWARM.length)];
  try { p.dimension.spawnEntity(what, { x: x + 0.5, y: y, z: z + 0.5 }); } catch {}
}

// ---------------------------------------------------------------------------
// the bunkers
// ---------------------------------------------------------------------------
function looksLikeSpruce(p) {
  let hits = 0;
  for (let i = 0; i < 26; i++) {
    const x = Math.floor(p.location.x + (Math.random() * 48 - 24));
    const z = Math.floor(p.location.z + (Math.random() * 48 - 24));
    const y = groundY(p.dimension, x, z, Math.floor(p.location.y) + 20);
    if (y === undefined) continue;
    for (let k = 0; k < 10; k++) {
      let b;
      try { b = p.dimension.getBlock({ x: x, y: y + k, z: z }); } catch { break; }
      if (!b) break;
      if (b.typeId.indexOf("spruce") >= 0 || b.typeId.indexOf("podzol") >= 0) { hits++; break; }
    }
    if (hits >= 3) return true;
  }
  return false;
}

function tryBunker(p) {
  if (nearASite(p.location, 380)) return;
  if (Math.random() > 0.04) return;
  if (!looksLikeSpruce(p)) return;

  const angle = Math.random() * Math.PI * 2;
  const away = 60 + Math.random() * 24;
  const x = Math.floor(p.location.x + Math.cos(angle) * away);
  const z = Math.floor(p.location.z + Math.sin(angle) * away);
  const y = groundY(p.dimension, x, z, Math.floor(p.location.y) + 30);
  if (y === undefined) return;

  const dim = p.dimension;
  try {
    const here = dim.getBlock({ x: x, y: y - 1, z: z });
    if (here && here.isLiquid) return;
    dim.runCommand(`execute positioned ${x} ${y - 1} ${z} run function bunker/build`);
  } catch { return; }
  rememberSite(x, y - 1, z);
  say("§8§oYou can smell old iron on the wind.");

  // the rest a moment later, so it is not all in one tick
  system.runTimeout(() => plantTrees(dim, x, y, z), 60);
  system.runTimeout(() => writeSigns(dim, x, y - 1, z), 100);
}

function plantTrees(dim, x, y, z) {
  const spots = [[27, 15], [-23, 21], [19, -25], [-29, -17], [35, -7], [-38, 4]];
  for (const [dx, dz] of spots) {
    const tx = x + dx, tz = z + dz;
    const ty = groundY(dim, tx, tz, y + 22);
    if (ty === undefined) continue;
    try { dim.runCommand(`execute positioned ${tx} ${ty - 1} ${tz} run function tree/giant`); } catch {}
  }
}

/*
  No Bedrock command can put words in a book, so the three lines go on three
  signs in the small room to the south instead. The block id for a plain sign
  has been spelled several different ways over the years, so this tries each
  one until one of them is a real block.
*/
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
  if (d === 2) say("§4§lDay 2. §r§7§oSomething came with the dark.");
  if (d === 3) say("§4§lDay 3. §r§7§oThey are not looking at you any more. They are looking through you.");
  if (d === 5) {
    say("§4§lDay 5. §r§7§oThere is almost nothing left alive. Listen.");
    try { dim.runCommand("gamerule domobspawning false"); } catch {}
  }
  if (d >= 6) {
    if (d === 6) say("§4§lDay 6. §r§7§oWhatever was hiding has stopped hiding.");
    try { dim.runCommand("gamerule domobspawning true"); } catch {}
  }
}

// ---------------------------------------------------------------------------
// the three clocks
// ---------------------------------------------------------------------------
system.runInterval(() => {
  try {
    const h = theHunter();
    if (h) reelIn(h); else grabbed.clear();
    if (tongueCooldown > 0) tongueCooldown--;
  } catch {}
}, 1);

system.runInterval(() => {
  try {
    const h = theHunter();
    if (!h) return;
    stareCheck(h);
    smash(h);
    tongue(h);
  } catch {}
}, 4);

system.runInterval(() => {
  try {
    checkDay();
    const d = day();
    const night = isNight();
    const h = theHunter();

    if (h && (!night || !overworlders().some(p => dist(p.location, h.location) < 120))) {
      hunterLeaves(h);
    } else if (!h && d >= 2 && night) {
      spawnHunter();
    }

    if (d >= 3 && night) turnSome();
    if (d >= 5) goQuiet();
    if (d === 5) cull();
    if (d >= 6 && night) swarm();

    for (const p of overworlders()) tryBunker(p);
  } catch {}
}, 20);

system.runInterval(() => {
  try { chaseTurned(); } catch {}
}, 4);

world.afterEvents.worldInitialize?.subscribe(() => {
  say("§4§lScopophobia§r§7§o is loaded. Nothing happens until day 2.");
});
