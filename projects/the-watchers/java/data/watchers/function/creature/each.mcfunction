# Every tick, for one Watcher. Run as it, standing where it is.
function watchers:creature/body

# A Watcher that is only watching stands still and stares. The moment it is
# out of your view it is taken away, so when you turn round it is not there.
execute if entity @s[tag=wt_watching] run function watchers:creature/watch
execute unless entity @s[tag=wt_watching] run function watchers:creature/hunt

# None of them are about in daylight. Whatever it was doing, dawn ends it.
execute if score #time wt_day matches ..12999 run function watchers:creature/leave
execute if score #time wt_day matches 22801.. run function watchers:creature/leave
execute unless entity @p[distance=..110] run function watchers:creature/leave
