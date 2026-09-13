# Day 3. A few more of them turn every second, and they do not turn back.
execute as @e[type=#watchers:turned,tag=!wt_turned,limit=4,sort=random] at @s if entity @p[distance=..44] run function watchers:mobs/mark
