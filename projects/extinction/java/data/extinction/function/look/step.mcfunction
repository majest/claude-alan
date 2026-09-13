scoreboard players add #ray ex_n 1
execute if entity @e[tag=ex_creature,distance=..1.9] run function extinction:creature/seen
execute unless entity @e[tag=ex_creature,distance=..1.9] if score #ray ex_n matches ..48 if block ~ ~ ~ #extinction:see_through positioned ^ ^ ^1 run function extinction:look/step
