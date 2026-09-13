# Pick one of eight directions and start looking for the ground. Close: a
# Watcher is meant to be plainly there and plainly looking at you, not a shape
# on the horizon.
scoreboard players set #drop wt_n 40
execute store result score #r wt_n run random value 0..7
execute if score #r wt_n matches 0 positioned ~12 ~10 ~ run function watchers:place/ground
execute if score #r wt_n matches 1 positioned ~9 ~10 ~9 run function watchers:place/ground
execute if score #r wt_n matches 2 positioned ~ ~10 ~12 run function watchers:place/ground
execute if score #r wt_n matches 3 positioned ~-9 ~10 ~9 run function watchers:place/ground
execute if score #r wt_n matches 4 positioned ~-12 ~10 ~ run function watchers:place/ground
execute if score #r wt_n matches 5 positioned ~-9 ~10 ~-9 run function watchers:place/ground
execute if score #r wt_n matches 6 positioned ~ ~10 ~-12 run function watchers:place/ground
execute if score #r wt_n matches 7 positioned ~9 ~10 ~-9 run function watchers:place/ground
