from ast import Raise


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_alive = False
        self.alive = False
        self.neighbors = []
    def add_neighbor(self, coords):
        self.neighbors.append(coords)

    def has_neighbor(self, x, y):
        return (x, y) in self.neighbors


class GameOfLife:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.grid = []

    def get_cell(self, x, y):
        for cell in self.grid:
            if cell.x == x and cell.y == y:
                return cell
        raise Exception("Cell not found at %d %d" % (x, y))

    def add_neighbors(self, cell):
        neighbors = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for neighbor in neighbors:
            x = cell.x + neighbor[0]
            y = cell.y + neighbor[1]
            if x >= 0 and x < self.width and y >= 0 and y < self.height:
                self.get_cell(x, y).add_neighbor((-neighbor[0], -neighbor[1]))

    def load_map(self, filename):
        with open(filename, "r") as f:
            f = f.readlines()
            self.height = len(f)
            self.width = len(f[0])
            self.grid = [Cell(x, y) for y in range(self.height) for x in range(self.width)]
            for y, line in enumerate(f):
                for x, char in enumerate(line):
                    if char == "#":
                        cell = self.get_cell(x, y)
                        cell.alive = True
                        self.add_neighbors(cell)

    def calculate_neighbors(self):
        for cell in self.grid:
            if cell.is_alive:
                self.add_neighbors(cell)
    def show_grid(self):
        if (len(self.grid) == 0):
            raise Exception("No grid loaded")
        print("\033c")
        table = [["  " for x in range(self.width)] for y in range(self.height)]
        for cell in self.grid:
            cell.is_alive = cell.alive
            cell.alive = False
            cell.neighbors = []
            if cell.is_alive:
                table[cell.y][cell.x] = "██"
        self.calculate_neighbors()
        frame = "__" * (self.width + 1) + "\n|"
        frame += "|\n|".join(["".join(row) for row in table])
        frame += "|"
        frame += "\n|" + "__" * self.width + "|"
        print(frame)
