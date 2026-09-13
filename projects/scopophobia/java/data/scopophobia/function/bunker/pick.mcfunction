# Put it well away from wherever the player is standing.
scoreboard players set #what sc_n 3
scoreboard players set #drop sc_n 90
execute store result score #r sc_n run random value 0..7
execute if score #r sc_n matches 0 positioned ~72 ~30 ~ run function scopophobia:place/ground
execute if score #r sc_n matches 1 positioned ~51 ~30 ~51 run function scopophobia:place/ground
execute if score #r sc_n matches 2 positioned ~ ~30 ~72 run function scopophobia:place/ground
execute if score #r sc_n matches 3 positioned ~-51 ~30 ~51 run function scopophobia:place/ground
execute if score #r sc_n matches 4 positioned ~-72 ~30 ~ run function scopophobia:place/ground
execute if score #r sc_n matches 5 positioned ~-51 ~30 ~-51 run function scopophobia:place/ground
execute if score #r sc_n matches 6 positioned ~ ~30 ~-72 run function scopophobia:place/ground
execute if score #r sc_n matches 7 positioned ~51 ~30 ~-51 run function scopophobia:place/ground
