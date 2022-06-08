import pygame
from pygame.locals import *
import time
import sys
from Classes import PlayerClass



class Player(PlayerClass):
    def __init__(self):
        super().__init__()
        self.hp = 3
        self.bullets = []
        self.bullet_cooldown = 0
        self.x = 0
        self.y = 800
        self.idle_relative = [1, 0]

    def display(self, screen):
        if abs(self.idle_relative[1]) >= 10:
            self.idle_relative[1] -= 0.1 * self.idle_relative[0]
            self.idle_relative[0] *= -1
        self.idle_relative[1] += self.idle_relative[0] * (15 - abs(self.idle_relative[1])) / 20
        for bullet in self.bullets:
            bullet[1] -= self.bullet_speed
            screen.blit(self.bullet, (bullet[0], bullet[1]))
            if bullet[1] < -100:
                self.bullets.remove(bullet)
        font = pygame.font.SysFont("Arial", 30)
        hp_text = font.render("HP: %d" % self.hp, True, (255, 255, 255))
        screen.blit(hp_text, (10, 10))
        screen.blit(self.costumes[self.costume // 5], (self.x, self.y + self.idle_relative[1]))
        self.costume = (self.costume + 1) % (len(self.costumes) * 5)

    def move_right(self):
        if self.x < 1150:
            self.x += self.player_speed

    def move_left(self):
        if self.x > 0:
            self.x -= self.player_speed

    def move_up(self):
        if self.y > 600:
            self.y -= self.player_speed

    def move_down(self):
        if self.y < 800:
            self.y += self.player_speed

    def shoot(self):
        if self.bullet_cooldown == 0:
            self.bullets.append([self.x + 45, self.y])
            self.bullet_cooldown = 20
