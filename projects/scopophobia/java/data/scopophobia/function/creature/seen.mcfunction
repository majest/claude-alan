# It knows you are looking. Run as the player who looked.
effect give @e[tag=sc_creature,limit=1] minecraft:speed 5 2 true
playsound minecraft:entity.warden.roar hostile @s ~ ~ ~ 0.8 1.8
title @s actionbar {"text":"it has seen you","color":"dark_red","italic":true}
