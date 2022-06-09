from ctypes.wintypes import WORD
import random
from re import X
from turtle import left
import pygame
import time
from Classes import Enemy

class Attack:
    img = pygame.image.load("assets/meteorite.png")
    img = pygame.transform.scale(img, (50, 50))
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class Enemies:
    def __init__(self) -> None:
        self.enemies = [[Enemy() for _ in range(15)] for _ in range(3)]
        self.lines_pos = [0, 0, 0]
        self.enemies_top = 0
        self.attacks = []

    def update(self, game):
        self.enemies_top += 0.3
        for i in range(3):
            self.lines_pos[i] += (1 if i % 2 else -1) * 2
            if abs(self.lines_pos[i]) > game.window_width:
                self.lines_pos[i] = 0
        for attack in self.attacks:
            attack.y += 5

    def display(self, game):
        for attack in self.attacks:
            game.screen.blit(attack.img, (attack.x, attack.y))
        for line_index, line in enumerate(self.enemies):
            for enemie_index, enemy in enumerate(line):
                if not enemy.alive:
                    continue
                x = self.lines_pos[line_index] + enemie_index * 80
                game.screen.blit(enemy.img, (x - game.window_width, self.enemies_top + line_index * 80))
                game.screen.blit(enemy.img, (x, self.enemies_top + line_index * 80))
                game.screen.blit(enemy.img, (x + game.window_width, self.enemies_top + line_index * 80))

    def check_attacks(self, player):
        for attack in self.attacks:
            if attack.y > 850:
                self.attacks.remove(attack)
                continue
            if attack.x <= player.x + 100 and player.x <= attack.x + 50 and attack.y + 50 >= player.y and player.y + 100 >= attack.y:
                self.attacks.remove(attack)
                player.hp -= 1
                continue

    def check_bullets(self, width, bullets):
        for line_index, line in enumerate(self.enemies):
            for enemie_index, enemy in enumerate(line):
                if not enemy.alive:
                    continue
                top = self.enemies_top + line_index * 80
                left = (self.lines_pos[line_index] + enemie_index * 80) % width
                right = (self.lines_pos[line_index] + enemie_index * 80 + 50) % width
                bottom = self.enemies_top + line_index * 80 + 50
                for bullet in bullets:
                    if bullet.y < top or bullet.y > bottom:
                        continue
                    if bullet.x >= left and bullet.x <= right:
                        enemy.alive = False
                        bullets.remove(bullet)

    def attack(self, screen):
        width, _ = screen.get_size()
        line = random.randint(0, 2)
        self.attacks.append(Attack(random.randint(0, width), self.enemies_top + line * 80))

    def count_enemies(self):
        count = 0
        for line in self.enemies:
            for enemy in line:
                if enemy.alive:
                    count += 1
        return count
