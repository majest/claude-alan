# Only climb if there is room overhead, and kill its falling speed, or gravity
# wins the argument two blocks up.
execute at @s if block ~ ~2 ~ #scopophobia:see_through if entity @p[distance=..40] run tp @s ~ ~0.22 ~
execute at @s if block ~ ~2 ~ #scopophobia:see_through if entity @p[distance=..40] run data merge entity @s {Motion:[0.0d,0.0d,0.0d],FallDistance:0.0f}
