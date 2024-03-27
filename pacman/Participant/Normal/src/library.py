PX = 32


class BadFileException(Exception):
    """Raised when the input file is not as expected"""
    # your code here


class Vector2D:
    """
    Implement the Vector2D class with the following methods:
    - __init__(self, x=0, y=0): constructor
    - __add__(self, other): add two vectors
    - __sub__(self, other): subtract two vectors
    - __mul__(self, other): dot product of two vectors
    - __abs__(self): length of the vector
    - __str__(self): string representation of the vector
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        # your code here

    def __sub__(self, other):
        # your code here

    def __mul__(self, other):
        # your code here

    def __abs__(self):  # length of the vector
        # your code here

    def __str__(self):
        # your code here


def load_from_file(file: str) -> list[list[str]]:
    """
    Load the game map from the file
    hint: use the open() and .strip() functions
    """
    game_map: list[list[str]] = []
    with open(file, 'r') as f:
        # your code here
    return game_map


def is_array_rectangular(game_map: list[list[str]]) -> bool:
    """
        Check if the 2D array is rectangular
        hint: use the len() function
        """
    width = len(game_map[0])
    for line in game_map:
        # your code here
    return True


def zip2d(game_map: list[list[str]], f: callable) -> None:
    """
    Iterate over the 2D array and apply the function f to each cell
    hint: use the enumerate() function
    """
    for i, row in enumerate(game_map):
        for j, cell in enumerate(row):
            f(i, j, cell)


def get_coordinates(x: int, y: int) -> tuple[int, int, int, int]:
    """
    Convert the coordinates to the pixel coordinates
    """
    x0 = x * PX
    y0 = y * PX
    x1 = x0 + PX
    y1 = y0 + PX
    return x0, y0, x1, y1


def get_position(game_map: list[list[str]], entity: str) -> Vector2D:
    """
    Get the position of the entity in the game map
    hint: you can use the zip2d() function to iterate over the game map
          you can also re-use the enumerate() function
          the two implementations are equivalent
    """
    for i, row in enumerate(game_map):
        for j, cell in enumerate(row):
            if cell == entity:
                # your code here
    raise BadFileException(f'Entity {entity} not found')
