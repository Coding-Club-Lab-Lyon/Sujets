import sys


def parser() -> tuple[int, int, list[list[str]]]:
    """
    Parse the input file
    :return: Tuple containing height, width and the map
    """
    if len(sys.argv) != 2:
        print("Usage: ./solver <file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()
        if len(lines) < 1 or len(lines[0].split()) != 2:
            print("Invalid input file format")
            sys.exit(1)

        try:
            height, width = map(int, lines[0].split())
        except ValueError:
            print("Invalid height or width values")
            sys.exit(1)

        bsq_map = [list(line.strip()) for line in lines[1:]]
    return height, width, bsq_map

