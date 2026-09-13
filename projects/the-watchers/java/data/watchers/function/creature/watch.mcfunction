# It does not move while it is watching.
data merge entity @s {Motion:[0.0d,0.0d,0.0d]}
scoreboard players add @s wt_hold 1
# nobody has looked at it for a while, or it has waited too long: it goes
execute if score @s wt_seen matches 1.. if score @s wt_hold matches 30.. run function watchers:creature/leave
execute if score @s wt_hold matches 1400.. run function watchers:creature/leave
