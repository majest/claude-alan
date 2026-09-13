# Pick one of eight directions, go that way, and start looking for the ground.
# Run this as a player, standing where they are.
scoreboard players set #drop ex_n 80
execute store result score #r ex_n run random value 0..7
execute if score #r ex_n matches 0 positioned ~44 ~26 ~ run function extinction:place/ground
execute if score #r ex_n matches 1 positioned ~31 ~26 ~31 run function extinction:place/ground
execute if score #r ex_n matches 2 positioned ~ ~26 ~44 run function extinction:place/ground
execute if score #r ex_n matches 3 positioned ~-31 ~26 ~31 run function extinction:place/ground
execute if score #r ex_n matches 4 positioned ~-44 ~26 ~ run function extinction:place/ground
execute if score #r ex_n matches 5 positioned ~-31 ~26 ~-31 run function extinction:place/ground
execute if score #r ex_n matches 6 positioned ~ ~26 ~-44 run function extinction:place/ground
execute if score #r ex_n matches 7 positioned ~31 ~26 ~-31 run function extinction:place/ground
