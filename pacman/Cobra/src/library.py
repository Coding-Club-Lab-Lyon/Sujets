PX = 32


class BadFileException(Exception):
    """Raised when the input file is not as expected"""
    def __init__(self, message: str):
        super().__init__(message)


class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def __abs__(self):  # length of the vector
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __str__(self):
        return f"Vector({self.x}, {self.y})"


def load_from_file(file: str) -> list[list[str]]:
    game_map: list[list[str]] = []
    with open(file, 'r') as f:
        for line in f:
            game_map.append(list(line.strip()))
    return game_map


def is_array_rectangular(game_map: list[list[str]]) -> bool:
    width = len(game_map[0])
    for line in game_map:
        if len(line) != width:
            return False
    return True


def zip2d(game_map: list[list[str]], f: callable) -> None:
    for i, row in enumerate(game_map):
        for j, cell in enumerate(row):
            f(i, j, cell)


def get_coordinates(x: int, y: int) -> tuple[int, int, int, int]:
    x0 = x * PX
    y0 = y * PX
    x1 = x0 + PX
    y1 = y0 + PX
    return x0, y0, x1, y1


def get_position(game_map: list[list[str]], entity: str) -> Vector2D:
    for i, row in enumerate(game_map):
        for j, cell in enumerate(row):
            if cell == entity:
                return Vector2D(j, i)
    raise BadFileException(f'Entity {entity} not found')
