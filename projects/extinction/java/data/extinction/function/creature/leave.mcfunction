particle minecraft:large_smoke ~ ~1 ~ 0.3 0.9 0.3 0.02 50 force
execute as @a[distance=..50] at @s run playsound minecraft:entity.warden.dig hostile @s ~ ~ ~ 0.6 0.6
function extinction:creature/cleanup
kill @s
