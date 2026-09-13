summon minecraft:zombie ~ ~ ~ {Tags:["sc_creature","sc_new"],Silent:1b,PersistenceRequired:1b,CanBreakDoors:1b,IsBaby:0b}
execute as @e[tag=sc_new,limit=1] at @s run function scopophobia:creature/setup
tag @e[tag=sc_new] remove sc_new
