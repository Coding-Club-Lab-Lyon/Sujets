import pygame

WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0] 
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
YELLOW = [255, 255, 0]
MAGENTA = [255, 0, 255]
CYAN = [0, 255, 255]

pygame.init()

window = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("Myce Paint")
leave = False
window.fill(WHITE)
fill = False
color = BLACK

def pick_color(key):
    if key ==  pygame.key.key_code('r'):
        return (RED)
    if key ==  pygame.key.key_code('g'):
        return (GREEN)
    if key ==  pygame.key.key_code('b'):
        return (BLUE)
    if key ==  pygame.key.key_code('j'):
        return (YELLOW)
    if key ==  pygame.key.key_code('m'):
        return (MAGENTA)
    if key ==  pygame.key.key_code('c'):
        return (CYAN)
    if key ==  pygame.key.key_code('e'):
        return (WHITE)
    else:
        return (BLACK)


while not leave: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            leave = True
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                leave = True
            elif event.key ==  pygame.key.key_code('f'):
                fill = True
            else:
                color = pick_color(event.key)
    if fill == True and pygame.mouse.get_pressed()[0]:
        window.fill(color)
        fill = False
    elif pygame.mouse.get_pressed()[0]:
        pos_x, pos_y = pygame.mouse.get_pos()
        pygame.draw.circle(window, color, [pos_x, pos_y], 5)
    pygame.display.update()

pygame.quit()
quit
