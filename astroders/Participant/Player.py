import pygame
from pygame.locals import *
from Classes import Bullet, PlayerClass

class Player(PlayerClass):
    def __init__(self):
        super().__init__()
        self.bullets = []
        self.bullet_cooldown = 0

    def update(self):
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1
        for bullet in self.bullets:
            bullet.y -= self.bullet_speed
            if bullet.x < -100:
                self.bullets.remove(bullet)

    def display(self, game):
        self.costume = (self.costume + 1) % (len(self.costumes) * 5)
        hp_text = game.font.render("HP: %d" % self.hp, True, (255, 255, 255))
        game.screen.blit(self.costumes[self.costume // 5], (self.x, self.y + self.idle_relative[1]))

    def shoot(self):
        if self.bullet_cooldown == 0:
            self.bullets.append(Bullet(self.x + 45, self.y))
            self.bullet_cooldown = 20

    def move_left(self):
        if self.x > 0:
            self.x -= self.player_speed
