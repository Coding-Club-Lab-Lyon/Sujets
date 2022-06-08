import random
import pygame

enemies_images = [
            "assets/feu.png",
            "assets/vent.png",
            "assets/terre.png",
            "assets/eau.png"
        ]

player_costumes = [
    "assets/serpentaire/serpentaire.png",
    "assets/serpentaire/serpentaire1.png",
    "assets/serpentaire/serpentaire2.png",
    "assets/serpentaire/serpentaire1.png",
]

class PlayerClass:
    def __init__(self) -> None:
        self.costumes = []
        for i in range(4):
            img = pygame.image.load(player_costumes[i])
            img = pygame.transform.scale(img, (100, 100))
            self.costumes.append(img)
        self.costume = 0
        self.player_speed = 5
        self.bullet_speed = 10
        self.bullet = pygame.image.load("assets/caducee.png")
        self.bullet = pygame.transform.scale(self.bullet, (10, 50))
        self.shooting_speed = 1

class EnemyClass:
    def __init__(self) -> None:
        self.img = pygame.image.load(random.choice(enemies_images))
        self.img = pygame.transform.scale(self.img, (50, 50))
