# A zombie underneath, because a data pack cannot invent a new mob. It is
# invisible; the shape you see is built out of block displays in creature/parts.
#
# Minecraft renamed every attribute in 1.21.2 — "generic.movement_speed" became
# "movement_speed". Both names are here on purpose: your version knows one of
# them and quietly ignores the other.
#
# scale 3 makes it three times the size of a player, hitbox and all.
attribute @s minecraft:scale base set 3
attribute @s minecraft:generic.scale base set 3
attribute @s minecraft:max_health base set 140
attribute @s minecraft:generic.max_health base set 140
attribute @s minecraft:movement_speed base set 0.3
attribute @s minecraft:generic.movement_speed base set 0.3
attribute @s minecraft:attack_damage base set 8
attribute @s minecraft:generic.attack_damage base set 8
attribute @s minecraft:follow_range base set 96
attribute @s minecraft:generic.follow_range base set 96
attribute @s minecraft:knockback_resistance base set 1
attribute @s minecraft:generic.knockback_resistance base set 1
attribute @s minecraft:step_height base set 2
attribute @s minecraft:generic.step_height base set 2
data merge entity @s {Health:140f}
effect give @s minecraft:invisibility infinite 1 true
effect give @s minecraft:fire_resistance infinite 1 true
scoreboard players set @s wt_hold 0
scoreboard players set @s wt_seen 0

# before day 3 it only stands and watches
execute if score #mode wt_n matches ..0 run tag @s add wt_watching
execute if score #mode wt_n matches ..0 run attribute @s minecraft:movement_speed base set 0
execute if score #mode wt_n matches ..0 run attribute @s minecraft:generic.movement_speed base set 0

function watchers:creature/parts
execute if score #mode wt_n matches 1.. as @a at @s run playsound minecraft:ambient.cave hostile @s ~ ~ ~ 0.7 0.4
