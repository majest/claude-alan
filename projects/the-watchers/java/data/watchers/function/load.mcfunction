# The Watchers — everything here is set up once, when the world loads.
scoreboard objectives add wt_day dummy
scoreboard objectives add wt_n dummy
scoreboard objectives add wt_hold dummy
scoreboard objectives add wt_seen dummy
team add wt_turned
team modify wt_turned color black
tellraw @a [{"text":"The Watchers","color":"dark_red","bold":true},{"text":" is loaded. Nothing for two days. Then something.","color":"gray","bold":false,"italic":true}]
