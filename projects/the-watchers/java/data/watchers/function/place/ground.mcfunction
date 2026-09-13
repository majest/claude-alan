# Step down one block at a time until there is something solid underfoot.
# This function calls itself, which is how you write a loop in Minecraft.
# #drop is how many steps are left, so it can never run away with itself.
scoreboard players remove #drop wt_n 1
execute if score #drop wt_n matches ..0 run function watchers:place/done
execute if score #drop wt_n matches 1.. if block ~ ~-1 ~ #watchers:see_through positioned ~ ~-1 ~ run function watchers:place/ground
execute if score #drop wt_n matches 1.. unless block ~ ~-1 ~ #watchers:see_through run function watchers:place/done
