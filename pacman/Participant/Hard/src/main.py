import sys
from Participant.Normal.src import wrapper as wp
from library import BadFileException


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 <map.txt>")
        exit(1)
    filename: str = sys.argv[1]
    try:
        app = wp.Wrapper(filename)
    except BadFileException as error:
        # handle the error
    # launch the app


if __name__ == '__main__':
    main()
