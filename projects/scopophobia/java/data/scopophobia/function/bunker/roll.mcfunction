# roughly one chance in twenty five, checked once a second
execute store result score #r sc_n run random value 1..25
execute if score #r sc_n matches 1 run function scopophobia:bunker/pick
