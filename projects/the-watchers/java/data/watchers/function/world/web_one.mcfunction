# Hang one web under whatever leaves are here, if any are.
execute if block ~ ~ ~ #minecraft:leaves if block ~ ~-1 ~ minecraft:air run setblock ~ ~-1 ~ minecraft:cobweb
execute if block ~ ~2 ~ #minecraft:leaves if block ~ ~1 ~ minecraft:air run setblock ~ ~1 ~ minecraft:cobweb
execute if block ~ ~4 ~ #minecraft:leaves if block ~ ~3 ~ minecraft:air run setblock ~ ~3 ~ minecraft:cobweb
