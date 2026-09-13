# Runs every single tick — twenty times a second. Keep it short.
execute store result score #day ex_day run time query day
execute store result score #time ex_day run time query daytime

# the creature, and anyone its tongue has hold of
execute as @e[tag=ex_creature] at @s run function extinction:creature/each
execute as @a[tag=ex_grabbed] at @s run function extinction:creature/pull
execute unless entity @e[tag=ex_creature] if entity @e[tag=ex_body] run function extinction:creature/cleanup

# things that do not need checking twenty times a second
scoreboard players add #n ex_n 1
execute if score #n ex_n matches 4.. if entity @e[tag=ex_creature] run function extinction:look/all
execute if score #n ex_n matches 4.. if score #day ex_day matches 3.. run function extinction:mobs/step
execute if score #n ex_n matches 4.. run scoreboard players set #n ex_n 0

scoreboard players add #s ex_n 1
execute if score #s ex_n matches 20.. run function extinction:second
