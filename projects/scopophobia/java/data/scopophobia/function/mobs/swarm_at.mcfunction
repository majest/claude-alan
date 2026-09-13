execute store result score #near sc_n if entity @e[type=#scopophobia:culled,distance=..55]
execute if score #near sc_n matches ..20 run function scopophobia:place/pick
