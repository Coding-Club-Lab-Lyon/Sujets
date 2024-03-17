import cc_maze as wrapper

map, PosY, PosX = wrapper.load_from_file("map.txt")


# Movement
def up():
    global map, PosY, PosX
    if PosY != 0 and map[PosY - 1][PosX] != "x":
        PosY -= 1


def down():
    global map, PosY, PosX
    if PosY != len(map) - 1 and map[PosY + 1][PosX] != "x":
        PosY += 1


def left():
    global map, PosY, PosX
    if PosX != 0 and map[PosY][PosX - 1] != "x":
        PosX -= 1


def right():
    global map, PosY, PosX
    if PosX != len(map[PosY]) - 1 and map[PosY][PosX + 1] != "x":
        PosX += 1


path = []


def algo(canvas):
    global map, PosY, PosX

    # Votre algorithme va ici.
    #
    # Vous pouvez utiliser la fonction update_grid du module cc_maze
    # pour mettre à jour l'affichage du labyrinthe dans votre algorithme.
    # Exemple:
    # wrapper.update_grid(canvas, map, PosY, PosX)


if __name__ == "__main__":
    window, canvas = wrapper.init_graphics(map, PosY, PosX)
    algo(canvas)
    window.mainloop()
