# Day 4. Most of the animals simply stop being there.
execute as @a at @s run kill @e[type=#watchers:turned,tag=!wt_turned,distance=30..96,limit=3,sort=random]
