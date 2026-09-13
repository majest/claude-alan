# Once a second.
scoreboard players set #s ex_n 0
function extinction:day/check
execute if score #tongue ex_n matches 1.. run scoreboard players remove #tongue ex_n 1

# day 2: it comes out at night, and there is only ever one of it
execute if score #day ex_day matches 2.. if score #time ex_day matches 13000..22800 unless entity @e[tag=ex_creature] run function extinction:creature/spawn

# day 3: the animals turn
execute if score #day ex_day matches 3.. if score #time ex_day matches 13000..22800 run function extinction:mobs/turn

# day 5: the world empties out and the music stops
execute if score #day ex_day matches 5.. run stopsound @a music
execute if score #day ex_day matches 5 run function extinction:mobs/cull

# day 6: far more of them than there should be
execute if score #day ex_day matches 6.. if score #time ex_day matches 13000..22800 run function extinction:mobs/swarm

# bunkers turn up in the old spruce forests
execute as @a at @s run function extinction:bunker/try
