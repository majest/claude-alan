# Does this player have the creature in view? Minecraft has no "can you see
# it" command, so this walks a line out from the player's eyes one block at a
# time until it hits the creature or hits something solid.
scoreboard players set #ray ex_n 0
execute anchored eyes positioned ^ ^ ^1 run function extinction:look/step
