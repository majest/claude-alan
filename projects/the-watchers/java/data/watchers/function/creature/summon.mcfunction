summon minecraft:zombie ~ ~ ~ {Tags:["wt_creature","wt_new"],Silent:1b,PersistenceRequired:1b,CanBreakDoors:1b,IsBaby:0b}
execute as @e[tag=wt_new,limit=1] at @s run function watchers:creature/setup
tag @e[tag=wt_new] remove wt_new
