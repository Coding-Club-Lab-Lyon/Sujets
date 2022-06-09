# from hashlib import new
import pygame
from pygame.locals import *
from Classes import Bullet, PlayerClass

class Player(PlayerClass):
    def __init__(self):
        super().__init__()
        self.bullets = []
        self.bullet_cooldown = 0
        self.hp = 3
        self.x = 0
        self.y = 800
        self.idle_relative = [1, 0]

    def update(self):
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1
        if abs(self.idle_relative[1]) >= 10:
            self.idle_relative[1] -= 0.1 * self.idle_relative[0]
            self.idle_relative[0] *= -1
        self.idle_relative[1] += self.idle_relative[0] * (15 - abs(self.idle_relative[1])) / 20
        for bullet in self.bullets:
            bullet.y -= self.bullet_speed
            if bullet.x < -100:
                self.bullets.remove(bullet)

    def display(self, game):
        hp_text = game.font.render("HP: %d" % self.hp, True, (255, 255, 255))
        self.costume = (self.costume + 1) % (len(self.costumes) * 5)
        for bullet in self.bullets:
            game.screen.blit(bullet.img, (bullet.x, bullet.y))
        game.screen.blit(hp_text, (10, 10))
        game.screen.blit(self.costumes[self.costume // 5], (self.x, self.y + self.idle_relative[1]))

    def shoot(self):
        if self.bullet_cooldown == 0:
            self.bullets.append(Bullet(self.x + 45, self.y))
            self.bullet_cooldown = 20

    def move_left(self):
        if self.x > 0:
            self.x -= self.player_speed

    def move_right(self):
        if self.x < 1100:
            self.x += self.player_speed

    def move_up(self):
        if self.y > 600:
            self.y -= self.player_speed

    def move_down(self):
        if self.y < 800:
            self.y += self.player_speed
