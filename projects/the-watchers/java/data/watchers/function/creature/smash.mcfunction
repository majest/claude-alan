# Wood, glass, leaves, grass and dirt, and nothing else. Stone, iron and
# obsidian all stop it dead, so a stone room is still worth building.
# The block it reaches for is the one at chest height in front of it, and if
# that is already gone, the one at its feet.
execute rotated ~ 0 positioned ^ ^1.3 ^0.8 if block ~ ~ ~ #watchers:soft run function watchers:creature/smash_it
execute rotated ~ 0 positioned ^ ^0.2 ^0.8 if block ~ ~ ~ #watchers:soft run function watchers:creature/smash_it
