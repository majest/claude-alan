# Extinction — everything here is set up once, when the world loads.
scoreboard objectives add ex_day dummy
scoreboard objectives add ex_n dummy
scoreboard objectives add ex_hold dummy
team add ex_turned
team modify ex_turned color black
tellraw @a [{"text":"Extinction","color":"dark_red","bold":true},{"text":" is loaded. Nothing happens until day 2.","color":"gray","bold":false,"italic":true}]
