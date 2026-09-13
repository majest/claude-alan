# has the day number changed since the last time we said anything?
execute unless score #shown wt_day = #day wt_day run function watchers:day/announce
