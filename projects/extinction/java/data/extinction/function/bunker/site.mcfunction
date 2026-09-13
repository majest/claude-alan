# We are standing on the ground where a bunker could go. Last checks: not in
# the sea, and not on top of one that is already there.
execute if entity @e[tag=ex_bunker,distance=..340] run return 0
execute if block ~ ~ ~ minecraft:water run return 0
function extinction:bunker/make
