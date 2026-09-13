# The jumpscare. One is put down three and a half blocks in front of your face,
# turned towards you, and taken away again about a second later. It does not
# touch you. It is just suddenly there.
#
# Two minutes before another, because a jumpscare you can predict is not one.
scoreboard players set @s wt_cool 120
scoreboard players set #what wt_n 5
scoreboard players set #drop wt_n 12
execute anchored eyes rotated ~ 0 positioned ^ ^ ^3.4 positioned ~ ~2 ~ run function watchers:place/ground
