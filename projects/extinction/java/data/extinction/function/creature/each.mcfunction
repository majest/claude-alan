# Every tick, for the creature. Run as the creature, standing where it is.
function extinction:creature/body
function extinction:creature/climb
execute if score #tongue ex_n matches ..0 if entity @p[distance=3..12] run function extinction:creature/tongue
# it goes when the sun comes up, or when there is nobody left to follow
execute if score #time ex_day matches ..12600 run function extinction:creature/leave
execute if score #time ex_day matches 22900.. run function extinction:creature/leave
execute unless entity @p[distance=..120] run function extinction:creature/leave
