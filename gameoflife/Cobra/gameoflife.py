from cc_gameoflife.core import *
import time

game = GameOfLife()
game.load_map("maps/planer.txt")

def count_neighbours(x, y):
    neighbors = 0
    if y > 0:
        neighbors += game.grid[y - 1][x]
        if x > 0:
            neighbors += game.grid[y - 1][x - 1]
        if x < game.width - 1:
            neighbors += game.grid[y - 1][x + 1]
    if y < game.height - 1:
        neighbors += game.grid[y + 1][x]
        if x > 0:
            neighbors += game.grid[y + 1][x - 1]
        if x < game.width - 1:
            neighbors += game.grid[y + 1][x + 1]
    if x > 0:
        neighbors += game.grid[y][x - 1]
    if x < game.width - 1:
        neighbors += game.grid[y][x + 1]
    return neighbors

while(True):
    game.show_grid()
    time.sleep(0.5)
    for y, line in enumerate(game.grid):
        for x, cell in enumerate(line):
            neighbors = count_neighbours(x, y)
            if (cell == 1):
                if (neighbors < 2):
                    game.next_grid[y][x] = 0
                elif (neighbors > 3):
                    game.next_grid[y][x] = 0
                else:
                    game.next_grid[y][x] = 1
            else:
                if (neighbors == 3):
                    game.next_grid[y][x] = 1
