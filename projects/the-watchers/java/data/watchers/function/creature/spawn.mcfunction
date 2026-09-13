# Put one on the ground close by — near enough to be seen, not near enough to
# touch. Before day 3 it only watches.
scoreboard players set #what wt_n 1
scoreboard players set #mode wt_n 0
execute if score #day wt_day matches 3.. if score #time wt_day matches 13000..22800 run scoreboard players set #mode wt_n 1
function watchers:place/pick
