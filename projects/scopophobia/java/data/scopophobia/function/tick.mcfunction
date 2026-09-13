# Runs every single tick — twenty times a second. Keep it short.
execute store result score #day sc_day run time query day
execute store result score #time sc_day run time query daytime

# the creature, and anyone its tongue has hold of
execute as @e[tag=sc_creature] at @s run function scopophobia:creature/each
execute as @a[tag=sc_grabbed] at @s run function scopophobia:creature/pull
execute unless entity @e[tag=sc_creature] if entity @e[tag=sc_body] run function scopophobia:creature/cleanup

# things that do not need checking twenty times a second
scoreboard players add #n sc_n 1
execute if score #n sc_n matches 4.. if entity @e[tag=sc_creature] run function scopophobia:look/all
execute if score #n sc_n matches 4.. if score #day sc_day matches 3.. run function scopophobia:mobs/step
execute if score #n sc_n matches 4.. run scoreboard players set #n sc_n 0

scoreboard players add #s sc_n 1
execute if score #s sc_n matches 20.. run function scopophobia:second
