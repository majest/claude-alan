scoreboard players operation #shown sc_day = #day sc_day
execute if score #day sc_day matches 2 run tellraw @a [{"text":"Day 2. ","color":"dark_red","bold":true},{"text":"Something came with the dark.","color":"gray","bold":false,"italic":true}]
execute if score #day sc_day matches 3 run tellraw @a [{"text":"Day 3. ","color":"dark_red","bold":true},{"text":"They are not looking at you any more. They are looking through you.","color":"gray","bold":false,"italic":true}]
execute if score #day sc_day matches 5 run tellraw @a [{"text":"Day 5. ","color":"dark_red","bold":true},{"text":"There is almost nothing left alive. Listen.","color":"gray","bold":false,"italic":true}]
execute if score #day sc_day matches 5 run gamerule doMobSpawning false
execute if score #day sc_day matches 6 run tellraw @a [{"text":"Day 6. ","color":"dark_red","bold":true},{"text":"Whatever was hiding has stopped hiding.","color":"gray","bold":false,"italic":true}]
execute if score #day sc_day matches 6.. run gamerule doMobSpawning true
