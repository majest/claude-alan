# Reel them in, a bit each tick. Run as the player being dragged.
scoreboard players remove @s sc_hold 1
execute if score @s sc_hold matches ..0 run tag @s remove sc_grabbed
execute unless entity @e[tag=sc_creature] run tag @s remove sc_grabbed
execute if entity @e[tag=sc_creature,distance=..1.6] run tag @s remove sc_grabbed
execute if entity @e[tag=sc_creature] facing entity @e[tag=sc_creature,limit=1,sort=nearest] feet positioned ^ ^ ^0.42 if block ~ ~ ~ #scopophobia:see_through run tp @s ~ ~ ~
particle minecraft:soul ~ ~1 ~ 0.2 0.3 0.2 0 2 force
