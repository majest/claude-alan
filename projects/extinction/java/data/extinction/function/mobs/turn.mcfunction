# Day 3. A few more of them turn every second, and they do not turn back.
execute as @e[type=#extinction:turned,tag=!ex_turned,limit=4,sort=random] at @s if entity @p[distance=..44] run function extinction:mobs/mark
