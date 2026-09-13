# A zombie underneath, because a data pack cannot invent a new mob from
# nothing. It is invisible, and the shape you see is built out of block
# displays in creature/parts.
#
# Minecraft renamed every attribute in 1.21.2 — "generic.movement_speed"
# became "movement_speed". Both names are here on purpose: your version
# knows one of them and quietly ignores the other.
attribute @s minecraft:max_health base set 60
attribute @s minecraft:generic.max_health base set 60
attribute @s minecraft:movement_speed base set 0.33
attribute @s minecraft:generic.movement_speed base set 0.33
attribute @s minecraft:attack_damage base set 8
attribute @s minecraft:generic.attack_damage base set 8
attribute @s minecraft:follow_range base set 80
attribute @s minecraft:generic.follow_range base set 80
attribute @s minecraft:knockback_resistance base set 0.9
attribute @s minecraft:generic.knockback_resistance base set 0.9
attribute @s minecraft:step_height base set 1.6
attribute @s minecraft:generic.step_height base set 1.6
data merge entity @s {Health:60f}
effect give @s minecraft:invisibility infinite 1 true
effect give @s minecraft:fire_resistance infinite 1 true
function scopophobia:creature/parts
execute as @a at @s run playsound minecraft:entity.warden.listening_angry hostile @s ~ ~ ~ 0.7 0.5
