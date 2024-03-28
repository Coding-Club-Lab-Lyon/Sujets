import sys
from Participant.Hard.src import wrapper as wp
from library import BadFileException


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 <map.txt>")
        exit(1)
    filename: str = sys.argv[1]
    try:
        app = wp.Wrapper(filename)
    except BadFileException as error:
        print(error)
        exit(1)
    app.run()


if __name__ == '__main__':
    main()
