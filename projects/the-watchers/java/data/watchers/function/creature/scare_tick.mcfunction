# It stands there for a little over a second and then it is not there.
scoreboard players add @s wt_hold 1
execute if score @s wt_hold matches 24.. run function watchers:creature/leave
