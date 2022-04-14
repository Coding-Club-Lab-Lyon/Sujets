class GameOfLife:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.grid = []
        self.next_grid = []

    def load_map(self, filename):
        with open(filename, "r") as f:
            f = f.readlines()
            self.height = len(f)
            self.width = len(f[0])
            self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
            self.next_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
            for y, line in enumerate(f):
                for x, char in enumerate(line):
                    if char == "#":
                        self.next_grid[y][x] = 1

    def show_grid(self):
        print("\033c")

        self.grid = self.next_grid
        self.next_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        frame = "__" * (self.width + 1)
        for y in range(self.height):
            frame += "\n|"
            for x in range(self.width):
                if self.grid[y][x] == 1:
                    frame += "██"
                else:
                    frame += "  "
            frame += "|"
        frame += "\n|" + "__" * self.width + "|"
        print(frame)
