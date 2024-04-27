import math
import tkinter as tk

from Bullet import Bullet
from Vector2D import Vector2D

MAX_BULLETS = 5
COOLDOWN = 10


class Player:
    """
    A class to represent a player.
    """
    def __init__(self, position: Vector2D, velocity: Vector2D, direction: int, size: int = 2, screen_width: int = 800,
                 screen_height: int = 600) -> None:
        """
        Constructs all the necessary attributes for the player object.
        :param position: position of the player
        :param velocity: velocity of the player
        :param direction: direction of the player
        :param size: size of the player representation
        :param screen_width: width of the screen
        :param screen_height: height of the screen
        """
        self.position = position
        self.velocity = velocity
        self.direction = direction
        self.size = size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_speed = 10
        self.bullets = []
        self.shoot_cooldown = 0

    def update(self, canvas: tk.Canvas) -> None:
        """
        Updates the player's position and direction.
        :param canvas: canvas to draw the player
        :return:
        """
        # Si tu aimes les maths, essaie de comprendre ce qui se passe ici.
        # Si tu détestes ca, c'est ta chance, tu peux ignorer les calculs
        self.position = Vector2D((self.position.x + self.velocity.x) % self.screen_width,
                                 (self.position.y + self.velocity.y) % self.screen_height)

        triangle = [
            (self.position.x, self.position.y - 10 * self.size),
            (self.position.x - 5 * self.size, self.position.y + 10 * self.size),
            (self.position.x + 5 * self.size, self.position.y + 10 * self.size),
        ]

        theta = math.radians(self.direction)
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)

        triangle = [
            (
                cos_theta * (x - self.position.x) - sin_theta * (y - self.position.y) + self.position.x,
                sin_theta * (x - self.position.x) + cos_theta * (y - self.position.y) + self.position.y,
            )
            for x, y in triangle
        ]

        # TODO: Créer un polygone pour représenter le joueur. Utilise la méthode create_polygon de canvas.
        pass

        # TODO: Met à jour les balles avec la méthode update de Bullet.
        pass
        # TODO: Filtrer les balles qui ne sont plus actives. (tips: utilise le type de retour de 'update')
        pass

        # tips: les deux étapes précédentes peuvent être faites en une seule ligne.

        # TODO: Met à jour le cooldown de tir.
        pass


    def accelerate(self, acceleration: int) -> None:
        """
        Update the player's velocity based on the acceleration.
        :param acceleration: delta velocity
        :return:
        """
        new_velocity = Vector2D(
            self.velocity.x + acceleration * math.sin(math.radians(self.direction)),
            self.velocity.y - acceleration * math.cos(math.radians(self.direction)),
        )
        speed = math.sqrt(new_velocity.x ** 2 + new_velocity.y ** 2) # Ici, on fait un calcul sur un vecteur qui pourrait être simplifié par ... une surcharge d'opérateur !

        # La ligne suivante sert à limiter la vitesse si celle ci dépasse la vitesse maximale. Utilise cette ligne
        #             new_velocity = Vector2D(new_velocity.x * self.max_speed / speed, new_velocity.y * self.max_speed / speed)
        # TODO: Limiter la vitesse du joueur à self.max_speed.
        pass

        self.velocity = new_velocity

    def shoot(self) -> None:
        """
        Shoot a bullet.
        :return:
        """
        # TODO: Ajouter une condition pour vérifier si le joueur peut tirer. (tips: utilise la macro MAX_BULLETS)

        bullet_speed = 10
        bullet_velocity = Vector2D(
            bullet_speed * math.sin(math.radians(self.direction)),
            -bullet_speed * math.cos(math.radians(self.direction))
        )

        # TODO: Créer une instance de Bullet et l'ajouter à la liste des balles.
        # bullet = ...
        pass
        # self.bullets.append(bullet) # A décommenter une fois que la balle est créée

        self.shoot_cooldown = COOLDOWN

    def rotate(self, angle: int) -> None:
        """
        Rotate the player.
        :param angle: angle to rotate
        :return:
        """
        # TODO: Modifier l'angle du joueur. (tips: utilise le type des attributs pour trouver le nom de l'attribut à modifier)
        pass
