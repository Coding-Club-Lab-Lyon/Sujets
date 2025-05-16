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

ERASER = (400, 400, 400)


# ----- Initialize the window -----
def initialize():
    pygame.init()
    window = pygame.display.set_mode((1080, 720))
    pygame.display.set_caption("Myce Paint")
    window.fill(WHITE)
    return window


# ----- Quit -----
def teardown():
    pygame.quit()


# ----- Pick the color -----
def pick_color(key):
    if key == pygame.key.key_code('r'):
        return (RED)
    if key == pygame.key.key_code('g'):
        return (GREEN)
    if key == pygame.key.key_code('b'):
        return (BLUE)
    if key == pygame.key.key_code('j'):
        return (YELLOW)
    if key == pygame.key.key_code('m'):
        return (MAGENTA)
    if key == pygame.key.key_code('c'):
        return (CYAN)
    if key == pygame.key.key_code('e'):
        return (WHITE)
    else:
        return (BLACK)


# ----- Draw a color palette -----
def color_palette(window, colors):
    # All the colors to print / select
    all_colors = [WHITE, BLACK, RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN, ERASER]
    # The position of the palette
    x = 5
    y = 10
    # Some other parameters
    size_rect = 32
    padding = 10
    # The rectangle for the palette (background)
    rect = pygame.Rect(0, 0, window.get_width(), size_rect + 2 * y)

    pygame.draw.rect(window, GRAY, rect)
    for i, color in enumerate(all_colors):
        rect_x = x + i * (size_rect + padding)
        rect = pygame.Rect(rect_x, y, size_rect, size_rect)
        if (color == ERASER):
            pygame.draw.line(window, BLACK, (rect.left+6, rect.bottom-6), (rect.right-6, rect.top+6), 4)
            pygame.draw.rect(window, BLACK, rect, 2)
        else:
            pygame.draw.rect(window, color, rect)
            pygame.draw.rect(window, BLACK, rect, 2)
        if colors == color:
            pygame.draw.rect(window, RED, rect, 3)

        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if rect.collidepoint(mouse_x, mouse_y):
                colors = color
    return colors


# ----- Draw Tool -----
def draw_tool(tool, window, rect, size_rect):
    if tool == "PEN":
        pygame.draw.circle(window, BLACK, rect.center, size_rect // 6)
    elif tool == "RECT":
        icon_rect = rect.inflate(-10, -15)
        pygame.draw.rect(window, BLACK, icon_rect, 2)
    elif tool == "CIRCLE":
        pygame.draw.circle(window, BLACK, rect.center, size_rect // 4, 2)


# ----- Draw a tool palette -----
def tool_palette(window, tools):
    # All the tools
    all_tools = ["PEN", "RECT", "CIRCLE"]
    # The position of the tools
    x = 5
    y = 10
    # Some other parameters
    size_rect = 32
    padding = 10
    # The rectangle for the palette (background)
    rect = pygame.Rect(0, 0, window.get_width(), size_rect + 2 * y)

    pygame.draw.rect(window, GRAY, rect)
    for i, tool in enumerate(all_tools):
        rect_x = x + i * (size_rect + padding)
        rect = pygame.Rect(rect_x, y, size_rect, size_rect)
        pygame.draw.rect(window, BLACK, rect, 2)
        # Draw tool icon
        draw_tool(tool, window, rect, size_rect)
        # Highlight if selected
        if tools == tool:
            pygame.draw.rect(window, RED, rect, 3)
        # Handle click
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if rect.collidepoint(mouse_x, mouse_y):
                tools = tool

    return tools


# ----- Print -----
def printer(fill, window, color, tool):
    if fill and pygame.mouse.get_pressed()[0]:
        if color == ERASER:
            window.fill(WHITE)
            fill = False
        else:
            window.fill(color)
            fill = False
    elif pygame.mouse.get_pressed()[0]:
        pos_x, pos_y = pygame.mouse.get_pos()

        if color == ERASER:
            window.fill(WHITE)
        else:
            if tool == "PEN":
                # Draw a small circle
                pygame.draw.circle(window, color, (pos_x, pos_y), 5)
            elif tool == "RECT":
                # Draw a rectangle
                rect_size = 30
                rect = pygame.Rect(pos_x, pos_y, rect_size, rect_size)
                pygame.draw.rect(window, color, rect, 2)
            elif tool == "CIRCLE":
                # Draw a circle
                pygame.draw.circle(window, color, (pos_x, pos_y), 20, 2)

    return fill


def main():
    window = initialize()
    running = True
    color = BLACK
    fill = False
    tool = "PEN"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.key.key_code('f'):
                    fill = True
                else:
                    color = pick_color(event.key)

        # NOTE: Change between color and tool else ...
        # color = color_palette(window, color)
        tool = tool_palette(window, tool)
        fill = printer(fill, window, color, tool)
        # Don't stay forever on the eraser :)
        if color == ERASER:
            color = BLACK
        pygame.display.update()

    teardown()


if __name__ == "__main__":
    main()
