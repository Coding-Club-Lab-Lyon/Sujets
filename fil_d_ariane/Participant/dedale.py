from time import sleep
import cc_maze
import sys

DELAY = 0.08  # in seconds

if len(sys.argv) != 2:
    print("Invalid arguments:\nPlease enter: python3 dedale.py <map>")
    exit(1)

map, PosY, PosX = cc_maze.load_from_file(sys.argv[1])
if map is None:
    print("No possible starting point found.")
    exit(1)


# Movement
def up():
    global canvas, map, PosY, PosX
    if PosY != 0 and map[PosY - 1][PosX] != "x":
        cc_maze.update_grid(canvas, PosX, PosY, "yellow")
        map[PosY][PosX] = '.'
        PosY -= 1
        cc_maze.update_grid(canvas, PosX, PosY, "blue")
        sleep(DELAY)


def down():
    global canvas, map, PosY, PosX
    if PosY != len(map) - 1 and map[PosY + 1][PosX] != "x":
        cc_maze.update_grid(canvas, PosX, PosY, "yellow")
        map[PosY][PosX] = '.'
        PosY += 1
        cc_maze.update_grid(canvas, PosX, PosY, "blue")
        sleep(DELAY)


def left():
    global canvas, map, PosY, PosX
    if PosX != 0 and map[PosY][PosX - 1] != "x":
        cc_maze.update_grid(canvas, PosX, PosY, "yellow")
        map[PosY][PosX] = '.'
        PosX -= 1
        cc_maze.update_grid(canvas, PosX, PosY, "blue")
        sleep(DELAY)


def right():
    global canvas, map, PosY, PosX
    if PosX != len(map[PosY]) - 1 and map[PosY][PosX + 1] != "x":
        cc_maze.update_grid(canvas, PosX, PosY, "yellow")
        map[PosY][PosX] = '.'
        PosX += 1
        cc_maze.update_grid(canvas, PosX, PosY, "blue")
        sleep(DELAY)


path = []


def algorithm(map):
    # Votre algorithme va ici.
    # Vous pouvez utiliser les fonctions de mouvement top, down, right, left.
    # Ces fonctions intéragissent directement avec l'affichage.
    # Une case déjà visitée sera transformée en '.' et affichée
    # en jaune sur l'écran.
    # Good luck!
    pass


if __name__ == "__main__":
    window, canvas = cc_maze.init_graphics(map, PosY, PosX)
    algorithm(map)
    window.mainloop()
