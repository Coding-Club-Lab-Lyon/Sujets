import tkinter as tk
import library as lib
import random

assets = '../assets/'
wall = '#'
pacgum = '.'
empty = '_'
door = 'X'
pacman = 'P'
blinky = 'B'


class SpriteHandler:
    def __init__(self, entity: str):
        self.entity = f'{entity}/'
        self.sprites: dict[str, tk.PhotoImage] = {
            'right1': tk.PhotoImage(file=f'{assets}{self.entity}right1.png'),
            'right2': tk.PhotoImage(file=f'{assets}{self.entity}right2.png'),
            'left1': tk.PhotoImage(file=f'{assets}{self.entity}left1.png'),
            'left2': tk.PhotoImage(file=f'{assets}{self.entity}left2.png'),
            'up1': tk.PhotoImage(file=f'{assets}{self.entity}up1.png'),
            'up2': tk.PhotoImage(file=f'{assets}{self.entity}up2.png'),
            'down1': tk.PhotoImage(file=f'{assets}{self.entity}down1.png'),
            'down2': tk.PhotoImage(file=f'{assets}{self.entity}down2.png'),
            'full': tk.PhotoImage(file=f'{assets}{self.entity}full.png'),
        }
        self.index = 0

    def get_sprite(self, direction: lib.Vector2D, use_full: bool) -> tk.PhotoImage:
        name = ''
        if direction.x == 1:
            name = 'right'
        elif direction.x == -1:
            name = 'left'
        elif direction.y == 1:
            name = 'down'
        elif direction.y == -1:
            name = 'up'
        if self.index >= 2 or self.index < 0:
            self.index = 0
            if use_full:
                return self.sprites.get('full')
        self.index += 1
        return self.sprites.get(f'{name}{self.index}')


class Entity:
    def __init__(self, name: str, map_representation: str, length: int, width: int, is_player: bool):
        self.is_player = is_player  # Handle special case for player
        self.direction = lib.Vector2D(1, 0)  # Direction vector
        self.sprite_handler = SpriteHandler(name)  # Handler for the sprites
        self.map_representation = map_representation  # Representation in the map, see macros above
        self.length = length  # Length of the map
        self.width = width  # Width of the map
        self.score = 0  # Score of the player
        self.last_value = empty  # Last value of the cell
        self.sprite_id = None  # Sprite ID, used to delete the sprite

    def move_player(self, game_map: list[list[str]]) -> None:
        """
        Move the player on the map
        """
        for i, row in enumerate(game_map):
            for j, cell in enumerate(row):
                if cell == self.map_representation:
                    # calculate the new position
                    new_i = 0  # your code here % self.length
                    new_j = 0  # your code here % self.width

                    # handle pacgum
                    if game_map[new_i][new_j] == pacgum:
                        pass
                        # your code here

                    # handle walls & doors
                    if game_map[new_i][new_j] == wall or game_map[new_i][new_j] == door:
                        pass
                        # your code here

                    # move the player on the map
                    game_map[i][j] = empty
                    # your code here
                    return

    def move(self, game_map: list[list[str]]) -> None:
        """
        Move the entity on the map
        """
        if self.is_player:
            return self.move_player(game_map)

        position = lib.get_position(game_map, self.map_representation)
        directions = [lib.Vector2D(0, 1), lib.Vector2D(0, -1), lib.Vector2D(1, 0), lib.Vector2D(-1, 0)]
        new_i = 0  # your code here % self.length
        new_j = 0  # your code here % self.width
        if game_map[new_i][new_j] == wall:
            pass
            #self.direction = # your code here // hint: random.choice()
        else:
            pass
            # tmp swap to store the last cell and update the current cell
            # move the entity on the map
            # your code here

    def draw(self, canvas: tk.Canvas, game_map: list[list[str]]) -> None:
        """
        Draw the entity on the canvas
        hint: use the get_sprite() function from the sprite handler
        """
        for i, row in enumerate(game_map):
            for j, cell in enumerate(row):
                if cell == self.map_representation:
                    x0, y0, x1, y1 = lib.get_coordinates(j, i)
                    # get the sprite
                    sprite = ""  # your code here
                    self.sprite_id = canvas.create_image(x0, y0, image=sprite, anchor='nw')


class Wrapper(tk.Tk):
    def __init__(self, filename: str):
        super().__init__()
        self.game_map = lib.load_from_file(filename)
        if not lib.is_array_rectangular(self.game_map):
            raise lib.BadFileException('Map is not rectangular')

        self.title('Pacman')
        self.geometry(f'{len(self.game_map[0]) * lib.PX}x{len(self.game_map) * lib.PX}')
        self.bind('<Key>', self.key_pressed)
        self.length = len(self.game_map)
        self.width = len(self.game_map[0])
        self.canvas = tk.Canvas(self, width=self.width * lib.PX, height=self.length * lib.PX)
        self.canvas.pack()

        self.pacgum = tk.PhotoImage(file=f'{assets}pacgum.png')
        self.entities = {
            'pacman': Entity('pacman', pacman, self.length, self.width, True),
        }
        self.is_game_over = False

    def key_pressed(self, event) -> None:
        """
        Handle the key pressed event
        hint: use the keycode attribute from the event
              use the direction attribute from the pacman entity
              use the print below to debug and find the keycode
        """
        if event.keycode == 38:
            self.quit()
        elif event.keycode == 111:
            pass
            # your code here
        elif event.keycode == 116:
            pass
            # your code here
        elif event.keycode == 113:
            pass
            # your code here
        elif event.keycode == 114:
            pass
            # your code here
        print(f'keycode: {event.keycode}')

    def draw_cell(self, i: int, j: int, cell: str) -> None:
        """
        This function is already implemented.
        """
        x0, y0, x1, y1 = lib.get_coordinates(j, i)
        if cell == wall or cell == door:
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='purple')
        elif cell == pacgum:
            self.canvas.create_image(x0, y0, image=self.pacgum, anchor='nw')
        else:
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='black')

    def draw_map(self) -> None:
        """
        Draw the map on the canvas
        hint: use the zip2d() function from the library
        """
        pass
        # add the argument to the function
        # lib.zip2d()

    def draw_text(self) -> None:
        """
        Draw the text on the canvas to show the score
        hint: get the score from the entity
        """
        # update the text
        self.canvas.create_text(10, 10,
                                text='', fill='white',
                                font=('Helvetica', '16', 'bold'), anchor='nw')

    def draw_entities(self) -> None:
        """
        Draw the entities on the canvas
        hint: look at the methods of the Entity class
              loop over the entities
        """
        for entity in self.entities.values():
            pass
            # your code here

    def move_entities(self) -> None:
        """
        Move the entities on the map
        hint: look at the methods of the Entity class
              loop over the entities
        """
        try:
            for entity in self.entities.values():
                pass
                # your code here
        except lib.BadFileException:
            self.is_game_over = True
            return

    def open_door(self) -> None:
        """
        Initialize the enemy ghost
        hint: create a new entity with the blinky representation
              take inspiration from the 'pacman' entity construction
        """
        for i, row in enumerate(self.game_map):
            for j, cell in enumerate(row):
                if cell == door:
                    self.game_map[i][j] = empty
        # your code here

    def run(self) -> None:
        self.after(5000, self.open_door)
        self.update()
        self.mainloop()

    def update(self) -> None:
        """
        Update the game state
        hint: call all the update methods of the Wrapper
        """
        self.canvas.delete('all')
        # your code here
        try:
            lib.get_position(self.game_map, pacman)
        except lib.BadFileException:
            self.is_game_over = True
            return
        if not self.is_game_over:
            self.after(300, self.update)
        else:
            self.canvas.delete(self.entities['pacman'].sprite_id)
            self.canvas.create_text(
                self.width * lib.PX // 2, self.length * lib.PX // 2, text='Game Over', fill='white',
                font=('Helvetica', '32', 'bold'), anchor='center')
