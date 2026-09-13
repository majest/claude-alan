# Cobwebs through the empty houses, so it looks left rather than tidy.
execute store result score #r wt_n run random value 0..7
execute positioned ~6 ~ ~4 run function watchers:world/web_here
execute positioned ~-8 ~ ~5 run function watchers:world/web_here
execute positioned ~3 ~ ~-9 run function watchers:world/web_here
execute positioned ~-5 ~ ~-6 run function watchers:world/web_here
execute positioned ~11 ~ ~-2 run function watchers:world/web_here
execute positioned ~-12 ~ ~8 run function watchers:world/web_here
