import random
import pygame

class Bullet:
    img = pygame.image.load("assets/caducee.png")
    img = pygame.transform.scale(img, (10, 50))
    def __init__(self, x = 0, y = 0) -> None:
        self.x = x
        self.y = y

class PlayerClass:
    player_costumes = [
    "assets/serpentaire/serpentaire.png",
    "assets/serpentaire/serpentaire1.png",
    "assets/serpentaire/serpentaire2.png",
    "assets/serpentaire/serpentaire1.png",
        ]
    def __init__(self) -> None:
        self.costumes = []
        for i in range(4):
            img = pygame.image.load(self.player_costumes[i])
            img = pygame.transform.scale(img, (100, 100))
            self.costumes.append(img)
        self.costume = 0
        self.player_speed = 5
        self.bullet_speed = 10
        self.shooting_speed = 1

class Enemy:
    enemies_images = [
            "assets/feu.png",
            "assets/vent.png",
            "assets/terre.png",
            "assets/eau.png"
        ]
    def __init__(self) -> None:
        self.img = pygame.image.load(random.choice(self.enemies_images))
        self.img = pygame.transform.scale(self.img, (50, 50))
        self.alive = True

class Game:
    def __init__(self) -> None:
        self.window_width = 1200
        self.window_height = 900
        self.running = True
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        background = pygame.image.load("assets/space.jpg")
        self.background = pygame.transform.scale(background, (self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        self.frame = 0
        self.win = False
        self.player = None
        self.enemies = None
        self.font = pygame.font.SysFont("Arial", 30)
