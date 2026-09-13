# Giant spruces around the bunker. #drop has to be wound back up before each
# one, because looking for the ground counts it down.
scoreboard players set #what wt_n 4
scoreboard players set #drop wt_n 50
execute positioned ~27 ~22 ~15 run function watchers:place/ground
scoreboard players set #drop wt_n 50
execute positioned ~-23 ~22 ~21 run function watchers:place/ground
scoreboard players set #drop wt_n 50
execute positioned ~19 ~22 ~-25 run function watchers:place/ground
scoreboard players set #drop wt_n 50
execute positioned ~-29 ~22 ~-17 run function watchers:place/ground
scoreboard players set #drop wt_n 50
execute positioned ~35 ~22 ~-7 run function watchers:place/ground
scoreboard players set #drop wt_n 50
execute positioned ~-38 ~22 ~4 run function watchers:place/ground
