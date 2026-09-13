# built by tools/make-functions.py — do not edit by hand
# Drag Watcher 3's body onto it, once a tick.
#
# There is no command for "turn this to the same angle as that", so a
# marker is parked eight blocks in front and every part is told to face
# it. rotated ~ 0 keeps the left-right angle and throws away the
# up-and-down one, so the body stays upright.
execute rotated ~ 0 positioned ^ ^ ^8 run tp @e[tag=wt_aim,tag=wt_p3,limit=1] ~ ~ ~
tp @e[tag=wt_torso,tag=wt_p3,limit=1] ~ ~ ~ facing entity @e[tag=wt_aim,tag=wt_p3,limit=1]
tp @e[tag=wt_head,tag=wt_p3,limit=1] ~ ~ ~ facing entity @e[tag=wt_aim,tag=wt_p3,limit=1]
tp @e[tag=wt_mouth,tag=wt_p3,limit=1] ~ ~ ~ facing entity @e[tag=wt_aim,tag=wt_p3,limit=1]
tp @e[tag=wt_armul,tag=wt_p3,limit=1] ~ ~ ~ facing entity @e[tag=wt_aim,tag=wt_p3,limit=1]
tp @e[tag=wt_armur,tag=wt_p3,limit=1] ~ ~ ~ facing entity @e[tag=wt_aim,tag=wt_p3,limit=1]
tp @e[tag=wt_armll,tag=wt_p3,limit=1] ~ ~ ~ facing entity @e[tag=wt_aim,tag=wt_p3,limit=1]
tp @e[tag=wt_armlr,tag=wt_p3,limit=1] ~ ~ ~ facing entity @e[tag=wt_aim,tag=wt_p3,limit=1]
tp @e[tag=wt_clawl,tag=wt_p3,limit=1] ~ ~ ~ facing entity @e[tag=wt_aim,tag=wt_p3,limit=1]
tp @e[tag=wt_clawr,tag=wt_p3,limit=1] ~ ~ ~ facing entity @e[tag=wt_aim,tag=wt_p3,limit=1]
tp @e[tag=wt_legul,tag=wt_p3,limit=1] ~ ~ ~ facing entity @e[tag=wt_aim,tag=wt_p3,limit=1]
tp @e[tag=wt_legur,tag=wt_p3,limit=1] ~ ~ ~ facing entity @e[tag=wt_aim,tag=wt_p3,limit=1]
tp @e[tag=wt_legll,tag=wt_p3,limit=1] ~ ~ ~ facing entity @e[tag=wt_aim,tag=wt_p3,limit=1]
tp @e[tag=wt_leglr,tag=wt_p3,limit=1] ~ ~ ~ facing entity @e[tag=wt_aim,tag=wt_p3,limit=1]
