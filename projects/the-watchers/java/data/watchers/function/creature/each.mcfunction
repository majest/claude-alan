# Every tick, for one Watcher. Run as it, standing where it is.
function watchers:creature/body

# A Watcher that is only watching stands still and stares. The moment it is
# out of your view it is taken away, so when you turn round it is not there.
execute if entity @s[tag=wt_watching] run function watchers:creature/watch
execute unless entity @s[tag=wt_watching] run function watchers:creature/hunt

execute unless entity @p[distance=..110] run function watchers:creature/leave
