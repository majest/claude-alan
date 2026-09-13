# "destroy" makes the block drop as an item and crack the way a mined one
# does, so you can hear it coming through the wall.
scoreboard players set @s wt_hold 12
setblock ~ ~ ~ minecraft:air destroy
particle minecraft:crit ~0.5 ~0.5 ~0.5 0.3 0.3 0.3 0.12 14 force
execute as @a[distance=..44] at @s run playsound minecraft:entity.zombie.break_wooden_door hostile @s ~ ~ ~ 0.5 0.6
