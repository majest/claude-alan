# roughly one chance in twenty five, checked once a second
execute store result score #r ex_n run random value 1..25
execute if score #r ex_n matches 1 run function extinction:bunker/pick
