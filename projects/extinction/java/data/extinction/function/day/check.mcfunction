# has the day number changed since the last time we said anything?
execute unless score #shown ex_day = #day ex_day run function extinction:day/announce
