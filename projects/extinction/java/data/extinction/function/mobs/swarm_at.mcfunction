execute store result score #near ex_n if entity @e[type=#extinction:culled,distance=..55]
execute if score #near ex_n matches ..20 run function extinction:place/pick
