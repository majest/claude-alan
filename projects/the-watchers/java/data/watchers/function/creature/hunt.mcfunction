function watchers:creature/climb
scoreboard players remove @s wt_hold 1
execute if score @s wt_hold matches ..0 run function watchers:creature/smash
execute if score #tongue wt_n matches ..0 if entity @p[distance=4..14] run function watchers:creature/tongue
