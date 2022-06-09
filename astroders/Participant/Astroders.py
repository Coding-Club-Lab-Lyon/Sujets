import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *
from Classes import Game
from Player import Player
from Enemies import Enemies

def key_inputs(player):
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        exit()

def check_events(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    key_inputs(game.player)

def update_game_elements(game):
    game.clock.tick(60)
    game.player.update()

def display_game_elements(game):
    game.screen.blit(game.background, (0, 0))
    pygame.display.update()

def main():
    pygame.init()
    game = Game()
    game.player = Player()
    game.enemies = Enemies()
    while game.running:
        check_events(game)
        update_game_elements(game)
        display_game_elements(game)

if __name__== "__main__":
    main()
