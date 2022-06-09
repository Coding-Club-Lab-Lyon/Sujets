import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *
from Classes import Game
from Player import Player
from Enemies import Enemies

def attack_on_tick(game):
    game.frame += 1
    if game.frame > 50:
        game.frame = 0
        game.enemies.attack(game.screen)

def key_inputs(player):
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        exit()
    if keys[K_SPACE]:
        player.shoot()
    if keys[K_RIGHT]:
        player.move_right()
    if keys[K_LEFT]:
        player.move_left()
    if keys[K_UP]:
        player.move_up()
    if keys[K_DOWN]:
        player.move_down()

def check_events(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    key_inputs(game.player)

def update_game_elements(game):
    game.clock.tick(60)
    game.player.update()
    game.enemies.update(game)

def check_hit_boxes(game):
    game.enemies.check_attacks(game.player)
    game.enemies.check_bullets(game.window_width, game.player.bullets)

def display_game_elements(game):
    game.screen.blit(game.background, (0, 0))
    game.player.display(game)
    game.enemies.display(game)
    pygame.display.update()

def check_end_conditions(game):
    if game.player.hp <= 0 or game.enemies.enemies_top > game.window_height - 150:
        game.running = False
    if game.enemies.count_enemies() == 0:
        game.win = True
        game.running = False

def main():
    pygame.init()
    game = Game()
    game.player = Player()
    game.enemies = Enemies()
    while game.running:
        check_events(game)
        attack_on_tick(game)
        update_game_elements(game)
        check_hit_boxes(game)
        display_game_elements(game)
        check_end_conditions(game)
    if game.win:
        print("Bravo mais t'es un gros con")
    else:
        print("Tu as perdu sale chien...")

if __name__== "__main__":
    main()
