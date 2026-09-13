# The tongue. Run as the creature, standing where it is.
scoreboard players set #tongue wt_n 6
particle minecraft:crimson_spore ~ ~1.7 ~ 0.15 0.15 0.15 0.01 40 force
execute as @a[distance=..40] at @s run playsound minecraft:entity.hoglin.attack hostile @s ~ ~ ~ 0.8 0.4
execute as @p[distance=3..12] run function watchers:creature/grab
