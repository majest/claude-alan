# Once a second.
scoreboard players set #s wt_n 0
function watchers:day/check
execute if score #tongue wt_n matches 1.. run scoreboard players remove #tongue wt_n 1

# how many of them are about
execute store result score #here wt_n if entity @e[tag=wt_creature]

# They only ever turn up after dark, and never in daylight. More of them in
# the old spruce forests, and more again from day 6.
execute if score #time wt_day matches 13000..22800 as @a at @s if score #here wt_n matches ..2 run function watchers:creature/maybe

# day 3: they stop watching. The raid waits for nightfall.
execute if score #day wt_day matches 3.. if score #time wt_day matches 13000..22800 if score #raid wt_n matches ..0 run function watchers:day/raid

# day 4: what is left of the animals comes for you
execute if score #day wt_day matches 4.. run function watchers:mobs/thin
execute if score #day wt_day matches 4.. if score #time wt_day matches 13000..22800 run function watchers:mobs/turn

# day 5: the music stops
execute if score #day wt_day matches 5.. run stopsound @a music

# bunkers, cobwebs, and villages nobody lives in any more
execute as @a at @s run function watchers:bunker/try
execute as @a at @s run function watchers:world/webs
execute as @a at @s run function watchers:world/village
