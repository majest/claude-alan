# Run as a player, and only ever at night — second.mcfunction will not call
# this while the sun is up. In the old spruce forests it is five times more
# likely than out in the open.
scoreboard players set #odds wt_n 2
execute if biome ~ ~ ~ minecraft:old_growth_spruce_taiga run scoreboard players set #odds wt_n 10
execute if biome ~ ~ ~ minecraft:old_growth_pine_taiga run scoreboard players set #odds wt_n 10
execute if biome ~ ~ ~ minecraft:taiga run scoreboard players set #odds wt_n 6
execute if score #day wt_day matches 6.. run scoreboard players add #odds wt_n 6
execute store result score #r wt_n run random value 1..100
execute if score #r wt_n <= #odds wt_n run function watchers:creature/spawn
