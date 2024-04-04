PX = 32


class BadFileException(Exception):
    """
    Raised when the input file is not as expected
    hint: use the super() function
    """
    def __init__(self, message: str):
        pass
        # your code here


class Vector2D:
    """
    Implement the Vector2D class with the following methods:
    - __init__(self, x=0, y=0): constructor
    - __add__(self, other): add two vectors
    - __sub__(self, other): subtract two vectors
    """
    def __init__(self, x=0, y=0):
        pass
        # your code here

    def __add__(self, other):
        pass
        # your code here

    def __sub__(self, other):
        pass
        # your code here


def load_from_file(file: str) -> list[list[str]]:
    """
    This function is already implemented.
    """
    game_map: list[list[str]] = []
    with open(file, 'r') as f:
        for line in f:
            game_map.append(list(line.strip()))
    return game_map


def is_array_rectangular(game_map: list[list[str]]) -> bool:
    """
    Check if the 2D array is rectangular
    hint: use the len() function
          compare the length of each line with the length of the first line
    """
    width = len(game_map[0])
    # your code here


def zip2d(game_map: list[list[str]], f: callable) -> None:
    """
    Apply the function f to each element of the 2D array
    hint: use the enumerate() function to loop over the array
    """
    pass
    # your code here


def get_coordinates(x: int, y: int) -> tuple[int, int, int, int]:
    """
    This function is already implemented.
    """
    x0 = x * PX
    y0 = y * PX
    x1 = x0 + PX
    y1 = y0 + PX
    return x0, y0, x1, y1


def get_position(game_map: list[list[str]], entity: str) -> Vector2D:
    """
    Get the position of the entity in the game map
    Raise a BadFileException if the entity is not found
    hint: you can re-use the enumerate() function
    """
    # your code here
    # if ... :
    return Vector2D(0, 0)
    # else :
    raise BadFileException(f'Entity {entity} not found')
