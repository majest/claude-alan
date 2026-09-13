summon minecraft:marker ~ ~ ~ {Tags:["wt_village"]}
particle minecraft:large_smoke ~ ~1 ~ 20 3 20 0.02 120 force
execute as @e[type=minecraft:villager,distance=..60] at @s run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 20 force
kill @e[type=minecraft:villager,distance=..60]
kill @e[type=minecraft:iron_golem,distance=..60]
tellraw @a[distance=..90] {"text":"Something has been through here.","color":"dark_gray","italic":true}
function watchers:world/village_webs
