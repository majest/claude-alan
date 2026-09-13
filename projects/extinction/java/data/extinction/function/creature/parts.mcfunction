# The shape you actually see. A data pack cannot add a new model, so the
# creature is built out of block displays — blocks with no hitbox, squashed
# and stretched into thin limbs. brightness holds them dark whatever the
# light is doing, except the mouth, which is left glowing.
summon minecraft:marker ~ ~ ~ {Tags:["ex_aim"]}
summon minecraft:block_display ~ ~ ~ {Tags:["ex_body","ex_torso"],block_state:{Name:"minecraft:black_concrete"},brightness:{sky:6,block:0},view_range:2.0f,transformation:{translation:[-0.15f,0.45f,-0.10f],scale:[0.30f,1.35f,0.20f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["ex_body","ex_head"],block_state:{Name:"minecraft:black_concrete"},brightness:{sky:6,block:0},view_range:2.0f,transformation:{translation:[-0.20f,1.78f,-0.18f],scale:[0.40f,0.42f,0.36f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["ex_body","ex_mouth"],block_state:{Name:"minecraft:white_concrete"},brightness:{sky:15,block:15},view_range:2.0f,transformation:{translation:[-0.075f,1.86f,0.18f],scale:[0.15f,0.15f,0.04f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["ex_body","ex_arml"],block_state:{Name:"minecraft:black_concrete"},brightness:{sky:6,block:0},view_range:2.0f,transformation:{translation:[-0.33f,0.60f,-0.05f],scale:[0.10f,1.15f,0.10f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["ex_body","ex_armr"],block_state:{Name:"minecraft:black_concrete"},brightness:{sky:6,block:0},view_range:2.0f,transformation:{translation:[0.23f,0.60f,-0.05f],scale:[0.10f,1.15f,0.10f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["ex_body","ex_clawl"],block_state:{Name:"minecraft:black_concrete"},brightness:{sky:6,block:0},view_range:2.0f,transformation:{translation:[-0.31f,0.10f,-0.03f],scale:[0.05f,0.52f,0.05f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["ex_body","ex_clawr"],block_state:{Name:"minecraft:black_concrete"},brightness:{sky:6,block:0},view_range:2.0f,transformation:{translation:[0.26f,0.10f,-0.03f],scale:[0.05f,0.52f,0.05f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
