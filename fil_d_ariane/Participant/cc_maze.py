import tkinter as tk

SQUARE_SIZE = 20
DELAY = 300
COLORS = {
    "x": "black",
    "-": "white",
    "o": "green",
    "P": "blue"
}


def load_from_file(path) -> (list[list[str]], int, int):
    map: list[list[str]] = []

    with open(path) as file:
        for line in file.readlines():
            map.append(list(line.rstrip()))
    for i, row in enumerate(map):
        for j, char in enumerate(row):
            if char == "-":
                return map, i, j
    exit(84)


def update_grid(canvas, map, PosY: int, PosX: int):
    for i in range(len(map)):
        for j in range(len(map[0])):
            if PosY == i and PosX == j:
                color = COLORS["P"]
            else:
                color = COLORS[map[i][j]]
            x0 = j * SQUARE_SIZE
            y0 = i * SQUARE_SIZE
            x1 = x0 + SQUARE_SIZE
            y1 = y0 + SQUARE_SIZE
            canvas.create_rectangle(x0, y0, x1, y1, fill=color)
    canvas.update()
    canvas.after(DELAY)


def init_graphics(map: list[list[str]], PosY, PosX):
    width = len(map[0]) * SQUARE_SIZE
    height = len(map) * SQUARE_SIZE
    window = tk.Tk()
    canvas = tk.Canvas(window, width=width, height=height)

    window.title("Participant: Fil d'Ariane")
    window.geometry(f"{width}x{height}")
    canvas.pack()
    update_grid(canvas, map, PosY, PosX)
    return window, canvas
