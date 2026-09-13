execute store result score #r sc_n run random value 0..5
execute if score #r sc_n matches 0 run summon minecraft:zombie ~ ~ ~
execute if score #r sc_n matches 1 run summon minecraft:skeleton ~ ~ ~
execute if score #r sc_n matches 2 run summon minecraft:spider ~ ~ ~
execute if score #r sc_n matches 3 run summon minecraft:creeper ~ ~ ~
execute if score #r sc_n matches 4 run summon minecraft:husk ~ ~ ~
execute if score #r sc_n matches 5 run summon minecraft:zombie ~ ~ ~
