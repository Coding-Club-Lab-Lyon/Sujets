#! /usr/bin/env python

import sys
import pygame

# Class for the orange dude
class Player:

    def __init__(self):
        self.rect = pygame.Rect(64, 64, 32, 32)
        self.sprite = pygame.image.load("./santa_top.png")
        self.sprite = pygame.transform.scale(self.sprite, (32, 32))

    def move(self, dx, dy):
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def change_animation(self, dir):
        self.sprite = pygame.image.load("./santa_" + dir + ".png")
        self.sprite = pygame.transform.scale(self.sprite, (32, 32))

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)

    def move_single_axis(self, dx, dy):
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy
        # If you collide with a wall, move out based on velocity
        new_sprite = "left"
        if dx > 0:
            new_sprite = "right"
        elif dx < 0:
            new_sprite = "left"
        elif dy > 0:
            new_sprite = "bottom"
        elif dy < 0:
            new_sprite = "top"
        self.change_animation(new_sprite)
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom


# Nice class to hold a wall rect
class Wall:

    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)


# Initialise pygame
pygame.init()

# Set up the display
pygame.display.set_caption("Get to the red square!")
screen = pygame.display.set_mode((640, 480))

clock = pygame.time.Clock()
walls = []  # List to hold the walls
player = Player()  # Create the player

# Holds the level layout in a list of strings.
map = open("map.txt", "r")
level = map.readlines()

# Parse the level string above. W = wall, E = exit
x = 0
y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            end_rect = pygame.Rect(x, y, 32, 32)
        x += 32
    y += 32
    x = 0

while 1:

    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)

    # Just added this to make it slightly fun ;)
    if player.rect.colliderect(end_rect):
        pygame.quit()
        sys.exit()

    # Draw the scene
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    player.draw(screen)
    # gfxdraw.filled_circle(screen, 255, 200, 5, (0,128,0))
    pygame.display.update()

pygame.quit()