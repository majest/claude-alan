# Runs every single tick — twenty times a second. Keep it short.
execute store result score #day wt_day run time query day
execute store result score #time wt_day run time query daytime

# the creature, and anyone its tongue has hold of
execute as @e[tag=wt_creature] at @s run function watchers:creature/each
execute as @a[tag=wt_grabbed] at @s run function watchers:creature/pull
execute unless entity @e[tag=wt_creature,tag=wt_p1] if entity @e[tag=wt_body,tag=wt_p1] run kill @e[tag=wt_p1,tag=!wt_creature]
execute unless entity @e[tag=wt_creature,tag=wt_p2] if entity @e[tag=wt_body,tag=wt_p2] run kill @e[tag=wt_p2,tag=!wt_creature]
execute unless entity @e[tag=wt_creature,tag=wt_p3] if entity @e[tag=wt_body,tag=wt_p3] run kill @e[tag=wt_p3,tag=!wt_creature]

# things that do not need checking twenty times a second
scoreboard players add #n wt_n 1
execute if score #n wt_n matches 4.. if entity @e[tag=wt_creature] run function watchers:look/all
execute if score #n wt_n matches 4.. if score #day wt_day matches 3.. run function watchers:mobs/step
execute if score #n wt_n matches 4.. run scoreboard players set #n wt_n 0

scoreboard players add #s wt_n 1
execute if score #s wt_n matches 20.. run function watchers:second
