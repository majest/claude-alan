# Drag the shape onto the invisible zombie, once every tick.
#
# There is no command for "turn this thing to the same angle as that thing",
# so instead a marker is parked eight blocks in front of the creature and
# every part is told to face the marker. rotated ~ 0 keeps the creature's
# left-right angle and throws away the up-down one, so the body stays upright.
execute rotated ~ 0 positioned ^ ^ ^8 run tp @e[tag=sc_aim,limit=1,sort=nearest] ~ ~ ~
tp @e[tag=sc_torso,limit=1,sort=nearest] ~ ~ ~ facing entity @e[tag=sc_aim,limit=1,sort=nearest]
tp @e[tag=sc_head,limit=1,sort=nearest] ~ ~ ~ facing entity @e[tag=sc_aim,limit=1,sort=nearest]
tp @e[tag=sc_mouth,limit=1,sort=nearest] ~ ~ ~ facing entity @e[tag=sc_aim,limit=1,sort=nearest]
tp @e[tag=sc_arml,limit=1,sort=nearest] ~ ~ ~ facing entity @e[tag=sc_aim,limit=1,sort=nearest]
tp @e[tag=sc_armr,limit=1,sort=nearest] ~ ~ ~ facing entity @e[tag=sc_aim,limit=1,sort=nearest]
tp @e[tag=sc_clawl,limit=1,sort=nearest] ~ ~ ~ facing entity @e[tag=sc_aim,limit=1,sort=nearest]
tp @e[tag=sc_clawr,limit=1,sort=nearest] ~ ~ ~ facing entity @e[tag=sc_aim,limit=1,sort=nearest]
