# Day 3. Three of them arrive already hunting, and they go for whatever you
# have built as much as for you.
scoreboard players set #raid wt_n 1
tellraw @a [{"text":"Day 3. ","color":"dark_red","bold":true},{"text":"They are not watching any more.","color":"gray","bold":false,"italic":true}]
scoreboard players set #mode wt_n 1
execute as @a at @s run function watchers:place/pick
execute as @a at @s run function watchers:place/pick
execute as @a at @s run function watchers:place/pick
execute as @a at @s run playsound minecraft:entity.warden.roar hostile @s ~ ~ ~ 1 0.6
