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

    map_width = len(map[0])
    map_height = len(map)

    while map[PosY][PosX] != 'o':
        print(map)
        if PosX + 1 < map_width and (map[PosY][PosX + 1] == '-'
                                     or map[PosY][PosX + 1] == 'o'):
            path.append("right")
            right()
        elif PosY + 1 < map_height and (map[PosY + 1][PosX] == '-'
                                        or map[PosY + 1][PosX] == 'o'):
            path.append("down")
            down()
        elif PosX - 1 >= 0 and (map[PosY][PosX - 1] == '-'
                                or map[PosY][PosX - 1] == 'o'):
            path.append("left")
            left()
        elif PosY - 1 >= 0 and (map[PosY - 1][PosX] == '-'
                                or map[PosY - 1][PosX] == 'o'):
            path.append("up")
            up()
        else:
            last_move = path.pop()
            if last_move == "right":
                left()
            elif last_move == "down":
                up()
            elif last_move == "left":
                right()
            elif last_move == "up":
                down()


if __name__ == "__main__":
    window, canvas = cc_maze.init_graphics(map, PosY, PosX)
    algorithm(map)
    window.mainloop()
