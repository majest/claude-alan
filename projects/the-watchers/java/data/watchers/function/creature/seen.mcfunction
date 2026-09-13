# Somebody is staring right at it. Run as the player who looked.
# Whatever it was doing, it is coming now.
tag @e[tag=wt_creature,limit=1,sort=nearest] remove wt_watching
scoreboard players set @e[tag=wt_creature,limit=1,sort=nearest] wt_seen 1
scoreboard players set @e[tag=wt_creature,limit=1,sort=nearest] wt_hold 0
effect give @e[tag=wt_creature,limit=1,sort=nearest] minecraft:speed 8 2 true
playsound minecraft:entity.warden.roar hostile @s ~ ~ ~ 0.9 1.5
title @s actionbar {"text":"it has seen you","color":"dark_red","italic":true}
