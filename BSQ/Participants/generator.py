import sys
import random # This may be useful ;)


def generate_bsq_file(height: int, width: int, filename: str) -> None:
    """
    Generate a file containing a random map
    :param height:
    :param width:
    :param filename:
    :return: None
    """
    pass # Replace by your implementation


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python generate_bsq.py <height> <width>")
        sys.exit(1)

    height: int = int(sys.argv[1])
    width: int = int(sys.argv[2])

    generate_bsq_file(height, width, f'maps/bsq_map_{height}x{width}.txt')


if __name__ == "__main__":
    main()
