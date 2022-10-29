# Space Invaders Overdrive
A simple space invaders game with one obtainable powerup. <br>
Use 'w','a','s','d' to move the spaceship around the screen, shoot with spacebar. <br>

Built to gain familiarity with simple game developement in python. <br>
Uses pygame as major underlying software to print everything to screen, manage images, create user events, etc. <br>
Uses threading to manage spawning of enemy_bullets, enemy_ships, and power_ups. <br>
<br>
Functions <br>
DRAW_GAME_WINDOW(hero, enemy_ships, friendly_bullets, enemy_bullets, lives, points, power_up_list, game_on) - <br>
HANDLE_HERO_MOVEMENT(keys_pressed, hero) - <br>
HANDLE_ENEMY_MOVEMENT(enemy_ships, hero, lives) - <br>
HANDLE_BULLETS(friendly_bullets, enemy_bullets, hero, enemy_ships, power_up_list) - <br> 
<br>
Threaded Functions: Each function here is threaded as they operate on their own timers. <br>
HANDLE_POWER_MOVEMENT(power-up-list) - when power up spawns, move it down accordingly. <br>
CREATE_ENEMY_BULLETS(enemy_ships, enemy_bullets) - for each enemy ship, spawn bullets. <br>
TRIPLE_SHIP(xvals, enemy_ships) - spawn enemy ships in sets of three using specified xvalues argument. <br>
