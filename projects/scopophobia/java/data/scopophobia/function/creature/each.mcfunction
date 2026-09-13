# Every tick, for the creature. Run as the creature, standing where it is.
function scopophobia:creature/body
function scopophobia:creature/climb
scoreboard players remove @s sc_hold 1
execute if score @s sc_hold matches ..0 run function scopophobia:creature/smash
execute if score #tongue sc_n matches ..0 if entity @p[distance=3..12] run function scopophobia:creature/tongue
# it goes when the sun comes up, or when there is nobody left to follow
execute if score #time sc_day matches ..12600 run function scopophobia:creature/leave
execute if score #time sc_day matches 22900.. run function scopophobia:creature/leave
execute unless entity @p[distance=..120] run function scopophobia:creature/leave
