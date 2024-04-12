import wrapper as wp
from library import BadFileException


def main():
    try:
        app = wp.Wrapper("../map.txt")
    except BadFileException as error:
        pass
        # handle the error
    # run the program


if __name__ == '__main__':
    main()
