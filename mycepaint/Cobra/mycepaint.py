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
    # pygame.display.set_caption("Myce Paint")
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


# ----- Draw Rectangle -----
def draw_rectangle(window, color, start_pos, current_pos):
    # Calculate dimensions
    width = current_pos[0] - start_pos[0]
    height = current_pos[1] - start_pos[1]

    # Create the rectangle
    rect = pygame.Rect(
        min(start_pos[0], current_pos[0]),
        min(start_pos[1], current_pos[1]),
        abs(width),
        abs(height)
    )

    # Draw the rectangle
    pygame.draw.rect(window, color, rect, 2)


# ----- Draw Circle -----
def draw_circle(window, color, start_pos, current_pos):
    # Calculate dimensions
    dx = current_pos[0] - start_pos[0]
    dy = current_pos[1] - start_pos[1]
    radius = int(max(abs(dx), abs(dy)) / 2)

    # Calculate center point
    center_x = start_pos[0] + dx // 2
    center_y = start_pos[1] + dy // 2

    # Draw the circle
    pygame.draw.circle(window, color, (center_x, center_y), radius, 2)


# ----- Print -----
def printer(fill, window, color, tool, start_pos, drawing):
    if fill and pygame.mouse.get_pressed()[0]:
        if color == ERASER:
            window.fill(WHITE)
            fill = False
        else:
            window.fill(color)
            fill = False
        return fill, None, False

    mouse_pressed = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()

    if color == ERASER and mouse_pressed:
        window.fill(WHITE)
        return fill, None, False

    if tool in ["RECT", "CIRCLE"]:
        # Start drawing - record start position
        if mouse_pressed and not drawing and start_pos is None:
            return fill, mouse_pos, True

        # Maintin state
        elif mouse_pressed and drawing and start_pos:
            return fill, start_pos, True

        # Finish the drawing when mouse is released
        elif not mouse_pressed and drawing and start_pos:
            if tool == "RECT":
                draw_rectangle(window, color, start_pos, mouse_pos)
            elif tool == "CIRCLE":
                draw_circle(window, color, start_pos, mouse_pos)
            return fill, None, False

    elif mouse_pressed:
        pos_x, pos_y = mouse_pos

        if tool == "PEN":
            pygame.draw.circle(window, color, (pos_x, pos_y), 5)

    return fill, start_pos, drawing


def main():
    window = initialize()
    running = True
    color = BLACK
    fill = False
    tool = "PEN"
    start_pos = None
    drawing = False

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

        # Uncomment to enable tool selection
        # color = color_palette(window, color)
        tool = tool_palette(window, tool)
        fill, start_pos, drawing = printer(fill, window, color, tool, start_pos, drawing)

        # Don't stay forever on the eraser :)
        if color == ERASER:
            color = BLACK
        pygame.display.update()

    teardown()


if __name__ == "__main__":
    main()
