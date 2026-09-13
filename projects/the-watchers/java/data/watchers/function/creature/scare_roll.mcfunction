# Run as a player, after dark, when they are not on cooldown.
# About four chances in a thousand each second, three times that in the forest.
scoreboard players set #odds wt_n 4
execute if biome ~ ~ ~ minecraft:old_growth_spruce_taiga run scoreboard players set #odds wt_n 11
execute if biome ~ ~ ~ minecraft:old_growth_pine_taiga run scoreboard players set #odds wt_n 11
execute store result score #r wt_n run random value 1..1000
execute if score #r wt_n <= #odds wt_n run function watchers:creature/scare
