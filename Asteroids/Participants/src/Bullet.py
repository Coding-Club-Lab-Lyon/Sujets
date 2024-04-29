import tkinter as tk
import math

from Vector2D import Vector2D


class Bullet:
    """
    A class to represent a bullet.
    """
    def __init__(self, position: Vector2D, velocity: Vector2D, direction: int) -> None:
        """
        Constructs all the necessary attributes for the bullet object.
        :param position: position of the bullet
        :param velocity: velocity of the bullet
        :param direction: direction of the bullet
        """
        self.position = position
        self.velocity = velocity
        self.direction = direction
        self.length = 10

    def update(self, canvas: tk.Canvas) -> bool:
        """
        Updates the bullet's position and direction.
        :param canvas: canvas to draw the bullet
        :return: True if the bullet is within the canvas, False otherwise
        """
        rotated_direction = (self.direction + 90) % 360
        end_point = Vector2D(
            self.position.x + self.length * math.cos(math.radians(rotated_direction)),
            self.position.y + self.length * math.sin(math.radians(rotated_direction))
        )

        # TODO: Créer la représentation graphique de la balle, utilise la méthode create_line du canvas
        pass

        self.position = Vector2D(
            (self.position.x + self.velocity.x),
            (self.position.y + self.velocity.y)
        )
        # TODO: Return True si la balle est toujours dans le canvas, False sinon
        pass
