scoreboard players operation #shown wt_day = #day wt_day
execute if score #day wt_day matches 2 run tellraw @a [{"text":"Day 2. ","color":"dark_red","bold":true},{"text":"There is something standing at the treeline.","color":"gray","bold":false,"italic":true}]
execute if score #day wt_day matches 4 run tellraw @a [{"text":"Day 4. ","color":"dark_red","bold":true},{"text":"The animals are wrong. Look at their eyes.","color":"gray","bold":false,"italic":true}]
execute if score #day wt_day matches 5 run tellraw @a [{"text":"Day 5. ","color":"dark_red","bold":true},{"text":"Listen. There is nothing to listen to.","color":"gray","bold":false,"italic":true}]
execute if score #day wt_day matches 6 run tellraw @a [{"text":"Day 6. ","color":"dark_red","bold":true},{"text":"There are more of them than there were.","color":"gray","bold":false,"italic":true}]
