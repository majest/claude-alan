# It goes. Only its own body goes with it, not anyone else's.
particle minecraft:large_smoke ~ ~2 ~ 0.5 1.4 0.5 0.02 60 force
execute if entity @s[tag=wt_p1] run kill @e[tag=wt_body,tag=wt_p1]
execute if entity @s[tag=wt_p1] run kill @e[tag=wt_aim,tag=wt_p1]
execute if entity @s[tag=wt_p2] run kill @e[tag=wt_body,tag=wt_p2]
execute if entity @s[tag=wt_p2] run kill @e[tag=wt_aim,tag=wt_p2]
execute if entity @s[tag=wt_p3] run kill @e[tag=wt_body,tag=wt_p3]
execute if entity @s[tag=wt_p3] run kill @e[tag=wt_aim,tag=wt_p3]
execute if entity @s[tag=wt_p4] run kill @e[tag=wt_body,tag=wt_p4]
execute if entity @s[tag=wt_p4] run kill @e[tag=wt_aim,tag=wt_p4]
kill @s
