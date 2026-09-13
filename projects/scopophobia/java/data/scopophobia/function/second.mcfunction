# Once a second.
scoreboard players set #s sc_n 0
function scopophobia:day/check
execute if score #tongue sc_n matches 1.. run scoreboard players remove #tongue sc_n 1

# day 2: it comes out at night, and there is only ever one of it
execute if score #day sc_day matches 2.. if score #time sc_day matches 13000..22800 unless entity @e[tag=sc_creature] run function scopophobia:creature/spawn

# day 3: the animals turn
execute if score #day sc_day matches 3.. if score #time sc_day matches 13000..22800 run function scopophobia:mobs/turn

# day 5: the world empties out and the music stops
execute if score #day sc_day matches 5.. run stopsound @a music
execute if score #day sc_day matches 5 run function scopophobia:mobs/cull

# day 6: far more of them than there should be
execute if score #day sc_day matches 6.. if score #time sc_day matches 13000..22800 run function scopophobia:mobs/swarm

# bunkers turn up in the old spruce forests
execute as @a at @s run function scopophobia:bunker/try
