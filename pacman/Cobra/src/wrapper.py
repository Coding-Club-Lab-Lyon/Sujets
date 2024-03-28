import tkinter as tk
import library as lib
import random

assets = './assets/'
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
        self.is_player = is_player
        self.direction = lib.Vector2D(1, 0)
        self.sprite_handler = SpriteHandler(name)
        self.map_representation = map_representation
        self.length = length
        self.width = width
        self.score = 0
        self.last_value = empty
        self.sprite_id = None

    def move_player(self, game_map: list[list[str]]) -> None:
        for i, row in enumerate(game_map):
            for j, cell in enumerate(row):
                if cell == self.map_representation:
                    new_i = (i + self.direction.y) % self.length
                    new_j = (j + self.direction.x) % self.width
                    if game_map[new_i][new_j] == pacgum:
                        self.score += 10
                    if game_map[new_i][new_j] == wall or game_map[new_i][new_j] == door:
                        return
                    game_map[i][j] = empty
                    game_map[new_i][new_j] = self.map_representation
                    return

    def move(self, game_map: list[list[str]]) -> None:
        if self.is_player:
            return self.move_player(game_map)

        position = lib.get_position(game_map, self.map_representation)
        directions = [lib.Vector2D(0, 1), lib.Vector2D(0, -1), lib.Vector2D(1, 0), lib.Vector2D(-1, 0)]
        new_i = (position.y + self.direction.y) % self.length
        new_j = (position.x + self.direction.x) % self.width
        if game_map[new_i][new_j] == wall:
            self.direction = random.choice(directions)
        else:
            tmp = game_map[new_i][new_j]
            game_map[position.y][position.x] = self.last_value
            self.last_value = tmp
            game_map[new_i][new_j] = self.map_representation

    def draw(self, canvas: tk.Canvas, game_map: list[list[str]]) -> None:
        for i, row in enumerate(game_map):
            for j, cell in enumerate(row):
                if cell == self.map_representation:
                    x0, y0, x1, y1 = lib.get_coordinates(j, i)
                    sprite = self.sprite_handler.get_sprite(self.direction, self.is_player)
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
        if event.keycode == 38:
            self.quit()
        elif event.keycode == 111:
            self.entities['pacman'].direction = lib.Vector2D(0, -1)
        elif event.keycode == 116:
            self.entities['pacman'].direction = lib.Vector2D(0, 1)
        elif event.keycode == 113:
            self.entities['pacman'].direction = lib.Vector2D(-1, 0)
        elif event.keycode == 114:
            self.entities['pacman'].direction = lib.Vector2D(1, 0)

    def draw_cell(self, i: int, j: int, cell: str) -> None:
        x0, y0, x1, y1 = lib.get_coordinates(j, i)
        if cell == wall or cell == door:
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='purple')
        elif cell == pacgum:
            self.canvas.create_image(x0, y0, image=self.pacgum, anchor='nw')
        else:
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='black')

    def draw_map(self) -> None:
        lib.zip2d(self.game_map, self.draw_cell)

    def draw_text(self) -> None:
        self.canvas.create_text(10, 10,
                                text=f'Score: {self.entities["pacman"].score}', fill='white',
                                font=('Helvetica', '16', 'bold'), anchor='nw')

    def draw_entities(self) -> None:
        for entity in self.entities.values():
            entity.draw(self.canvas, self.game_map)

    def move_entities(self) -> None:
        try:
            for entity in self.entities.values():
                entity.move(self.game_map)
        except lib.BadFileException:
            self.is_game_over = True
            return

    def open_door(self) -> None:
        for i, row in enumerate(self.game_map):
            for j, cell in enumerate(row):
                if cell == door:
                    self.game_map[i][j] = empty
        self.entities['blinky'] = Entity('blinky', blinky, self.length, self.width, False)

    def run(self) -> None:
        self.after(5000, self.open_door)
        self.update()
        self.mainloop()

    def update(self) -> None:
        self.canvas.delete('all')
        self.draw_map()
        self.draw_text()
        self.draw_entities()
        self.move_entities()
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
