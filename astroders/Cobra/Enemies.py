import random
import pygame
import time
from Classes import EnemyClass

class Enemy(EnemyClass):
    def __init__(self) -> None:
        super().__init__()
        self.alive = True


class Enemies:
    def __init__(self) -> None:
        self.enemies = [[Enemy() for _ in range(15)] for _ in range(3)]
        self.lines_pos = [0, 0, 0]
        self.enemies_top = 0
        self.attacks = []
        self.attack_image = pygame.image.load("assets/meteorite.png")
        self.attack_image = pygame.transform.scale(self.attack_image, (50, 50)) 

    def move_lines(self, width):
        self.enemies_top += 0.3
        for i in range(3):
            self.lines_pos[i] += (1 if i % 2 else -1) * 2
            if abs(self.lines_pos[i]) > width:
                self.lines_pos[i] = 0
    def display(self, screen):
        width, _ = screen.get_size()
        self.move_lines(width)
        for i, attack in enumerate(self.attacks):
            self.attacks[i][1] += 5
            screen.blit(self.attack_image, (attack[0], attack[1]))
        for i, line in enumerate(self.enemies):
            for base in [-width, 0, width]:
                for j, enemy in enumerate(line):
                    if not enemy.alive:
                        continue
                    screen.blit(enemy.img, (self.lines_pos[i] + base + j * 80, self.enemies_top + i * 80))
    def check_attacks(self, player):
        for attack in self.attacks:
            if attack[1] > 850:
                self.attacks.remove(attack)
            if attack[0] > player.x and attack[0] < player.x + 100 and attack[1] > player.y and attack[1] < player.y + 100:
                self.attacks.remove(attack)
                player.hp -= 1

    def check_bullets(self, width, bullets):
        for i, line in enumerate(self.enemies):
            for base in [-width, 0, width]:
                for j, enemy in enumerate(line):
                    if not enemy.alive:
                        continue
                    enemy_bounds = {
                        'top': self.enemies_top + i * 80,
                        'left': self.lines_pos[i] + base + j * 80,
                        'right': self.lines_pos[i] + base + j * 80 + 50,
                        'bottom': self.enemies_top + i * 80 + 50
                    }
                    for bullet in bullets:
                        if bullet[1] < enemy_bounds['top'] or bullet[1] > enemy_bounds['bottom']:
                            continue
                        if bullet[0] > enemy_bounds['left'] and bullet[0] < enemy_bounds['right']:
                            enemy.alive = False
                            bullets.remove(bullet)
    def attack(self, screen):
        width, _ = screen.get_size()
        line = random.randint(0, 2)
        self.attacks.append([random.randint(0, width), self.enemies_top + line * 80])

    def count_enemies(self):
        count = 0
        for line in self.enemies:
            for enemy in line:
                if enemy.alive:
                    count += 1
        return count
