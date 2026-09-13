# Scopophobia — everything here is set up once, when the world loads.
scoreboard objectives add sc_day dummy
scoreboard objectives add sc_n dummy
scoreboard objectives add sc_hold dummy
team add sc_turned
team modify sc_turned color black
tellraw @a [{"text":"Scopophobia","color":"dark_red","bold":true},{"text":" is loaded. Nothing happens until day 2.","color":"gray","bold":false,"italic":true}]
