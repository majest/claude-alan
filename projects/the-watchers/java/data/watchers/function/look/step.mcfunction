scoreboard players add #ray wt_n 1
execute if entity @e[tag=wt_creature,distance=..1.9] run function watchers:creature/seen
execute unless entity @e[tag=wt_creature,distance=..1.9] if score #ray wt_n matches ..48 if block ~ ~ ~ #watchers:see_through positioned ^ ^ ^1 run function watchers:look/step
