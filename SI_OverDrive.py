# A space invaders game created in order to learn more about the pygame library
# Version 0.03
# Noob
# May 22nd, 2021

import pygame
import os
import threading
import random
import time
import numpy as np

pygame.font.init()

# Start screen & Dimensions
pygame.init()
WIDTH, HEIGHT = 650, 650
SHIP_WIDTH, SHIP_HEIGHT = 45, 50
POWER_WIDTH, POWER_HEIGHT = 40, 40
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Overdrive")

# Colors & Fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
ORANGE = (255, 140, 0)

TITLE_FONT = pygame.font.SysFont('newyork', 50)
SUBTITLE_FONT = pygame.font.SysFont('arial', 40)
OPTIONS_FONT = pygame.font.SysFont('timesnewroman', 20)

POINT_LIVE_FONT = pygame.font.SysFont('Arial', 25)
END_FONT = pygame.font.SysFont('comicsans', 25)

# FPS/Speeds/Options
FPS = 60
VEL = 3
BULLET_VEL = 7
MAX_BULLETS = 5

# User created events
HERO_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 2
POWER_UP = pygame.USEREVENT + 3

# Imported Images
HERO_SHIP = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
HERO_SHIP = pygame.transform.rotate(pygame.transform.scale(HERO_SHIP, (SHIP_WIDTH, SHIP_HEIGHT)), 180)
ENEMY_SHIP = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
ENEMY_SHIP = pygame.transform.scale(ENEMY_SHIP, (SHIP_WIDTH, SHIP_HEIGHT))
BACKGROUND = pygame.image.load(os.path.join('Assets', 'space.png'))
BACKGROUND = pygame.transform.rotate(pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT)), 270)
POWERUP = pygame.image.load(os.path.join('Assets', 'liquor.png')).convert_alpha()
POWERUP = pygame.transform.scale(POWERUP, (POWER_WIDTH, POWER_HEIGHT))


def draw_game_window(hero, enemy_ships, friendly_bullets, enemy_bullets, lives, points, power_up_list, game_on):
    # Basic Background
    WIN.blit(BACKGROUND, (0, 0))
    bottom_bar = pygame.Rect(0, HEIGHT - 30, WIDTH, 30)
    pygame.draw.rect(WIN, BLACK, bottom_bar)
    
    # Points and lives
    points_text = POINT_LIVE_FONT.render("Points: %s" % points, 1, WHITE)
    lives_text = POINT_LIVE_FONT.render("Lives: %s" % lives, 1, WHITE)

    WIN.blit(points_text, (WIDTH - points_text.get_width() - 10, HEIGHT - 30))
    WIN.blit(lives_text, (10, HEIGHT - 30))
    
    # Hero/Enemies/Bullets
    WIN.blit(HERO_SHIP, (hero.x, hero.y))
    for enemy in enemy_ships:
        WIN.blit(ENEMY_SHIP, (enemy.x, enemy.y))
        
    for bullet in friendly_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in enemy_bullets:
        pygame.draw.rect(WIN, MAGENTA, bullet)
        
    for power in power_up_list:
        WIN.blit(POWERUP, (power.x, power.y))
        
    if game_on == False:
        end_text = END_FONT.render("Congrats you finished with a whopping %s points" % points, 1, WHITE)
        WIN.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height()))
        pygame.display.update()
        time.sleep(5)
        pass
        
    pygame.display.update()

    
# Control ship movement
def handle_hero_movement(keys_pressed, hero):
    if keys_pressed[pygame.K_d] and hero.x + SHIP_WIDTH + VEL < WIDTH:
        hero.x += VEL
    if keys_pressed[pygame.K_a] and hero.x - VEL > 0:
        hero.x -= VEL
    if keys_pressed[pygame.K_w] and hero.y - VEL > 0:
        hero.y -= VEL
    if keys_pressed[pygame.K_s] and hero.y + SHIP_HEIGHT + VEL < HEIGHT - 30:
        hero.y += VEL
        

def handle_enemy_movement(enemy_ships, hero, lives):
    for enemy in enemy_ships:
        if enemy.y < HEIGHT - 50:
            enemy.y += VEL // 2
        elif hero.colliderect(enemy):
            lives -= 1
            enemy_ships.remove(enemy)
        else: 
            lives -= 1
            enemy_ships.remove(enemy)


# Move bullets and update on collision
def handle_bullets(friendly_bullets, enemy_bullets, hero, enemy_ships, power_up_list):
    for bullet in friendly_bullets:
        bullet.y -= BULLET_VEL
        if bullet.y < -10:
            friendly_bullets.remove(bullet)
        for power in power_up_list:
            if power.colliderect(bullet):
                pygame.event.post(pygame.event.Event(POWER_UP))
                power_up_list.remove(power)
                friendly_bullets.remove(bullet)
        # Work to improve this portion's speed later on <-- DONT FORGET 
        for enemy in enemy_ships:
            if enemy.colliderect(bullet):
                pygame.event.post(pygame.event.Event(ENEMY_HIT))
                friendly_bullets.remove(bullet)
                enemy_ships.remove(enemy)
            elif enemy.colliderect(hero):
                pygame.event.post(pygame.event.Event(HERO_HIT))
                enemy_ships.remove(enemy)

    for bullet in enemy_bullets:
        bullet.y += BULLET_VEL
        if hero.colliderect(bullet):
            pygame.event.post(pygame.event.Event(HERO_HIT))
            enemy_bullets.remove(bullet)
        elif bullet.y >= HEIGHT + 10:
            enemy_bullets.remove(bullet)

            
# Manage power up movement
def handle_power_movement(power_up_list):
    for power in power_up_list:
        if power.y < HEIGHT - 50:
            power.y += 1
        else:
            power_up_list.remove(power)
    

# Thread one's function
def create_enemy_bullets(enemy_ships, enemy_bullets):
    for enemy in enemy_ships:
        bullet = pygame.Rect(enemy.x + enemy.width - 10, enemy.y + enemy.height // 2, 3, 10)
        enemy_bullets.append(bullet)

        
# Thread two's functions
def triple_ship(xvals, enemy_ships):
    for val in xvals:
        new_enemy = pygame.Rect(val, 0 - SHIP_HEIGHT, SHIP_WIDTH, SHIP_HEIGHT)
        new_enemy_left = pygame.Rect(val - 55, 0 - SHIP_HEIGHT * 2 + 10, SHIP_WIDTH, SHIP_HEIGHT)
        new_enemy_right = pygame.Rect(val + 55, 0 - SHIP_HEIGHT * 2 + 10, SHIP_WIDTH, SHIP_HEIGHT)
        enemy_ships.append(new_enemy)
        enemy_ships.append(new_enemy_left)
        enemy_ships.append(new_enemy_right)
        time.sleep(3)


def create_enemy_ships(enemy_ships, spawnmodes): 
    n = random.randint(0, int(len(spawnmodes) - 1))
    xvals = np.linspace(SHIP_WIDTH * 2 + 55, WIDTH - SHIP_WIDTH * 2 - 55, 5)
    con_div_xvals = [xvals[0], xvals[4], xvals[1], xvals[3], xvals[2]]
    
    if spawnmodes[n] == 'acrossleft':
        triple_ship(xvals, enemy_ships)
    elif spawnmodes[n] == 'acrossright':
        triple_ship(xvals[::-1], enemy_ships)
    elif spawnmodes[n] == 'converge':
        triple_ship(con_div_xvals, enemy_ships)
    elif spawnmodes[n] == 'diverge':
        triple_ship(con_div_xvals[::-1], enemy_ships)    
    

# First thread in order to spawn enemy bullets
def enemy_bullet_spawner(timer_varbinds):
    enemy_ships = timer_varbinds[0]
    enemy_bullets = timer_varbinds[1]
    create_enemy_bullets = timer_varbinds[2]
    while True:
        create_enemy_bullets(enemy_ships, enemy_bullets)
        time.sleep(1.5)

        
# Second thread in order to spawn enemy ships
def ship_spawner(ship_varbinds):
    enemy_ships = ship_varbinds[0]
    create_enemy_ships = ship_varbinds[1]
    spawnmodes = ship_varbinds[2]
    while True:
        create_enemy_ships(enemy_ships, spawnmodes)
        time.sleep(7)

        
# Third thread for power ups
def power_up_spawner(power_up_list):
    while True:
        rand_time = random.randint(25, 35)
        time.sleep(rand_time)
        n = random.randint(SHIP_WIDTH * 2 + 55, WIDTH - SHIP_WIDTH * 2 - 55)
        power_up = pygame.Rect(n, -20, POWER_WIDTH, POWER_HEIGHT)
        power_up_list.append(power_up)
        

# Exit all screens and pygame
def exit_all():
    pygame.display.quit()
    pygame.quit()
    exit()

    
def main():
    clock = pygame.time.Clock()
    # Point/health system initialization
    points = 0
    lives = 3
    
    # Hero ship initialization
    hero = pygame.Rect(WIDTH // 2 - SHIP_WIDTH // 2, HEIGHT - SHIP_HEIGHT - 45, SHIP_WIDTH, SHIP_HEIGHT)

    # Check if power up activated
    power_up_on = False
    
    # Generate empty arrays for objects
    enemy_ships = []
    friendly_bullets = []
    enemy_bullets = []
    power_up_list = []
    spawnmodes = ['acrossleft', 'acrossright', 'diverge', 'converge']
    
    enemy_bullet_varbinds = [enemy_ships, enemy_bullets, create_enemy_bullets]
    ship_varbinds = [enemy_ships, create_enemy_ships, spawnmodes]
    
    # Create 3 threads for timed spawning of enemy ships/bullets/power ups
    t1 = threading.Thread(target=enemy_bullet_spawner, group=None, args=(enemy_bullet_varbinds,), daemon=True)
    t2 = threading.Thread(target=ship_spawner, group=None, args=(ship_varbinds,), daemon=True)
    t3 = threading.Thread(target=power_up_spawner, group=None, args=(power_up_list,), daemon=True)
    t1.start()
    t2.start()
    t3.start()
    
    game_on = True
    while game_on:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or lives <= 0:
                game_on = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(friendly_bullets) <= MAX_BULLETS and power_up_on:
                    bullet = pygame.Rect(hero.x + hero.width - 10, hero.y + hero.height // 2 - 2, 3, 10)
                    bullet2 = pygame.Rect(hero.x + 10, hero.y + hero.height // 2 - 2, 3, 10)
                    friendly_bullets.append(bullet)
                    friendly_bullets.append(bullet2)
                elif event.key == pygame.K_SPACE and len(friendly_bullets) <= MAX_BULLETS:
                    bullet = pygame.Rect(hero.x + hero.width - 10, hero.y + hero.height // 2 - 2, 3, 10)
                    friendly_bullets.append(bullet)
                    
            if event.type == HERO_HIT:
                lives -= 1
            if event.type == ENEMY_HIT:
                points += 10
                
            if event.type == POWER_UP:
                power_up_on = True
                
        keys_pressed = pygame.key.get_pressed()
        handle_hero_movement(keys_pressed, hero)
        handle_enemy_movement(enemy_ships, hero, lives)
        handle_power_movement(power_up_list)  
        handle_bullets(friendly_bullets, enemy_bullets, hero, enemy_ships, power_up_list)
        draw_game_window(hero, enemy_ships, friendly_bullets, enemy_bullets, lives, points, power_up_list, game_on)
                
    exit_all()
                
        
if __name__ == "__main__":
    main()
