from cc_gameoflife.core import *
import time

game = GameOfLife()
game.load_map("maps/glider_gun.txt")
game.show_grid()
time.sleep(0.5)

while(True):
    for cell in game.grid:
        neighbors = 0
        if cell.has_neighbor(0, 1):
            neighbors += 1
        if cell.has_neighbor(1, 1):
            neighbors += 1
        if cell.has_neighbor(1, 0):
            neighbors += 1
        if cell.has_neighbor(1, -1):
            neighbors += 1
        if cell.has_neighbor(0, -1):
            neighbors += 1
        if cell.has_neighbor(-1, -1):
            neighbors += 1
        if cell.has_neighbor(-1, 0):
            neighbors += 1
        if cell.has_neighbor(-1, 1):
            neighbors += 1
        if (cell.last_alive):
            if (neighbors < 2):
                cell.alive = False
            elif (neighbors > 3):
                cell.alive = False
            else:
                cell.alive = True
        else:
            if (neighbors == 3):
                cell.alive = True
    game.show_grid()
    time.sleep(0.5)
