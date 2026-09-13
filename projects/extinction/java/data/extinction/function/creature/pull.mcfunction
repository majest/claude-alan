# Reel them in, a bit each tick. Run as the player being dragged.
scoreboard players remove @s ex_hold 1
execute if score @s ex_hold matches ..0 run tag @s remove ex_grabbed
execute unless entity @e[tag=ex_creature] run tag @s remove ex_grabbed
execute if entity @e[tag=ex_creature,distance=..1.6] run tag @s remove ex_grabbed
execute if entity @e[tag=ex_creature] facing entity @e[tag=ex_creature,limit=1,sort=nearest] feet positioned ^ ^ ^0.42 if block ~ ~ ~ #extinction:see_through run tp @s ~ ~ ~
particle minecraft:soul ~ ~1 ~ 0.2 0.3 0.2 0 2 force
