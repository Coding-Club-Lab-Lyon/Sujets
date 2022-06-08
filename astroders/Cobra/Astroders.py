import pygame
from pygame.locals import *
from Player import Player
from Enemies import Enemies

pygame.init()
window_width = 1200
window_height = 900
running = True
screen = pygame.display.set_mode((window_width, window_height))

background = pygame.image.load("assets/space.jpg")
background = pygame.transform.scale(background, (window_width, window_height))
clock = pygame.time.Clock()

player = Player()
enemies = Enemies()

def key_inputs():
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT]:
        player.move_right()
    if keys[K_LEFT]:
        player.move_left()
    if keys[K_UP]:
        player.move_up()
    if keys[K_DOWN]:
        player.move_down()
    if keys[K_SPACE]:
        player.shoot()

while running:
    clock.tick(60)
    dt = clock.get_time() / 1000
    if dt % 10:
        enemies.attack()
    for event in pygame.event.get():
        if pygame.key.get_pressed()[K_ESCAPE]:
            running = False
        if event.type == pygame.QUIT:
            running = False

    key_inputs()
    screen.blit(background, (0, 0))
    if player.bullet_cooldown > 0:
        player.bullet_cooldown -= 1
    player.display(screen)
    enemies.display(screen)
    enemies.check_bullets(window_width, player.bullets)
    pygame.display.update()
