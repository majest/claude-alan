# Bunkers turn up in the spruce forests, and never near another one.
# Run as a player, standing where they are.
execute if entity @e[tag=wt_bunker,distance=..380] run return 0
execute if biome ~ ~ ~ minecraft:old_growth_spruce_taiga run function watchers:bunker/roll
execute if biome ~ ~ ~ minecraft:old_growth_pine_taiga run function watchers:bunker/roll
execute if biome ~ ~ ~ minecraft:taiga run function watchers:bunker/roll
