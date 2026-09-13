# has the day number changed since the last time we said anything?
execute unless score #shown sc_day = #day sc_day run function scopophobia:day/announce
