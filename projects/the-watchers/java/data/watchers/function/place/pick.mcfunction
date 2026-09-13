# Pick one of eight directions and start looking for the ground. Close, because
# a Watcher is meant to be standing there when you turn round.
scoreboard players set #drop wt_n 60
execute store result score #r wt_n run random value 0..7
execute if score #r wt_n matches 0 positioned ~20 ~14 ~ run function watchers:place/ground
execute if score #r wt_n matches 1 positioned ~14 ~14 ~14 run function watchers:place/ground
execute if score #r wt_n matches 2 positioned ~ ~14 ~20 run function watchers:place/ground
execute if score #r wt_n matches 3 positioned ~-14 ~14 ~14 run function watchers:place/ground
execute if score #r wt_n matches 4 positioned ~-20 ~14 ~ run function watchers:place/ground
execute if score #r wt_n matches 5 positioned ~-14 ~14 ~-14 run function watchers:place/ground
execute if score #r wt_n matches 6 positioned ~ ~14 ~-20 run function watchers:place/ground
execute if score #r wt_n matches 7 positioned ~14 ~14 ~-14 run function watchers:place/ground
