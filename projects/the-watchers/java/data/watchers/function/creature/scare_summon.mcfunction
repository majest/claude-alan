# Run at the spot in front of the player, still as the player.
scoreboard players set #mode wt_n 0
summon minecraft:zombie ~ ~ ~ {Tags:["wt_creature","wt_new","wt_scare"],Silent:1b,PersistenceRequired:1b,IsBaby:0b}
execute as @e[tag=wt_new,limit=1] at @s run function watchers:creature/setup
tag @e[tag=wt_new] remove wt_new
execute as @e[tag=wt_scare,limit=1,sort=nearest] at @s run tp @s ~ ~ ~ facing entity @p
playsound minecraft:entity.warden.roar hostile @s ~ ~ ~ 1 1.9
effect give @s minecraft:darkness 2 0 true
effect give @s minecraft:nausea 4 0 true
title @s actionbar {"text":"!","color":"dark_red","bold":true}
