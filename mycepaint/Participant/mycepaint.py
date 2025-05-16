import pygame

# ----- Define Colors -----
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
YELLOW = [255, 255, 0]
MAGENTA = [255, 0, 255]
CYAN = [0, 255, 255]
GRAY = [230, 230, 230]


# écrit ton code ici :
# ----- Initialize -----
def initialize():
    pygame.init()


# ----- Quit -----
def teardown():
    pygame.quit()


def main():
    initialize()
    teardown()


# Attention ne dépasse pas !
if __name__ == "__main__":
    main()
