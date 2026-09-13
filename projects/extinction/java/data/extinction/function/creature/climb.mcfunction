# Wall climbing. A zombie cannot climb, so this does it by hand: if there is
# something solid right in front of its chest, haul it upwards a fraction of a
# block. Every tick, that is a thing walking up the side of your house.
# rotated ~ 0 keeps which way it is facing and throws away up-or-down, so it
# tests the wall in front of it rather than the floor.
execute rotated ~ 0 positioned ^ ^0.6 ^0.75 unless block ~ ~ ~ #extinction:see_through run function extinction:creature/climb_up
