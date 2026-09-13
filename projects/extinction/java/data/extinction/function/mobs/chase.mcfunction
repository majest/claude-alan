# A cow has no idea how to attack you, and a data pack cannot teach it. So it
# gets shoved towards you a little at a time instead, and bites when it
# arrives. The block check stops them walking through walls.
scoreboard players remove @s ex_hold 1
execute facing entity @p[distance=..28] feet rotated ~ 0 positioned ^ ^ ^0.17 if block ~ ~ ~ #extinction:see_through run tp @s ~ ~ ~
execute if entity @p[distance=..1.8] if score @s ex_hold matches ..0 run function extinction:mobs/bite
