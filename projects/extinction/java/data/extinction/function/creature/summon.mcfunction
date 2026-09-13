summon minecraft:zombie ~ ~ ~ {Tags:["ex_creature","ex_new"],Silent:1b,PersistenceRequired:1b,CanBreakDoors:1b,IsBaby:0b}
execute as @e[tag=ex_new,limit=1] at @s run function extinction:creature/setup
tag @e[tag=ex_new] remove ex_new
