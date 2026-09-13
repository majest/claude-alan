# Cobwebs in the spruce canopy. Run as a player, standing where they are.
execute unless biome ~ ~ ~ minecraft:old_growth_spruce_taiga unless biome ~ ~ ~ minecraft:old_growth_pine_taiga run return 0
execute store result score #r wt_n run random value 1..3
execute if score #r wt_n matches 1 positioned ~12 ~8 ~-9 run function watchers:world/web_one
execute if score #r wt_n matches 2 positioned ~-11 ~11 ~7 run function watchers:world/web_one
execute if score #r wt_n matches 3 positioned ~6 ~14 ~13 run function watchers:world/web_one
