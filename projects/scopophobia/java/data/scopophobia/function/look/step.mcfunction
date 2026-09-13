scoreboard players add #ray sc_n 1
execute if entity @e[tag=sc_creature,distance=..1.9] run function scopophobia:creature/seen
execute unless entity @e[tag=sc_creature,distance=..1.9] if score #ray sc_n matches ..48 if block ~ ~ ~ #scopophobia:see_through positioned ^ ^ ^1 run function scopophobia:look/step
