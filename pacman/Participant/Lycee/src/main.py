import wrapper as wp
from library import BadFileException


def main():
    try:
        app = wp.Wrapper("../map.txt")
    except BadFileException as error:
        print(error)
        exit(1)
    app.run()


if __name__ == '__main__':
    main()
