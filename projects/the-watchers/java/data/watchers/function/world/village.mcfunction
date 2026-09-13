# Villages nobody lives in any more. Run as a player, standing where they are.
# Once a village has been emptied a marker stays behind so it is not done twice.
execute if entity @e[tag=wt_village,distance=..70] run return 0
execute unless entity @e[type=minecraft:villager,distance=..50,limit=2] run return 0
execute store result score #r wt_n run random value 1..10
execute if score #r wt_n matches 9.. run function watchers:world/spared
execute if score #r wt_n matches ..8 run function watchers:world/empty_it
