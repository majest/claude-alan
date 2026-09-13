# built by tools/make-functions.py — do not edit by hand
# Give this Watcher the first slot nobody else is using.
execute unless entity @e[tag=wt_p1] run function watchers:creature/parts_1
execute unless entity @s[tag=wt_p1] unless entity @e[tag=wt_p2] run function watchers:creature/parts_2
execute unless entity @s[tag=wt_p1] unless entity @s[tag=wt_p2] unless entity @e[tag=wt_p3] run function watchers:creature/parts_3
execute unless entity @s[tag=wt_p1] unless entity @s[tag=wt_p2] unless entity @s[tag=wt_p3] unless entity @e[tag=wt_p4] run function watchers:creature/parts_4
