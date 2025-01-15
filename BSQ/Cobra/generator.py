import sys
import random


def generate_bsq_file(height: int, width: int, filename: str) -> None:
    with open(filename, 'w') as f:
        f.write(f"{height} {width}\n")
        for _ in range(height):
            line = ''.join(random.choice(['.', 'o']) for _ in range(width))
            f.write(line + '\n')


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python generate_bsq.py <height> <width>")
        sys.exit(1)

    height: int = int(sys.argv[1])
    width: int = int(sys.argv[2])

    generate_bsq_file(height, width, f'maps/bsq_map_{height}x{width}.txt')


if __name__ == "__main__":
    main()
