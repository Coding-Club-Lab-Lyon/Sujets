import random

from matplotlib import pyplot as plt
from matplotlib import animation


class Viewer():
    def __init__(self) -> None:
        self.x = []
        self.y = []
        pass

    def append(self, el):
        if (len(self.x) + len(self.y)) % 2 == 0:
            self.x.append(el)
        else:
            self.y.append(el)

    def __sep_point(self):
        li = [[], [], [], []]
        for i, j in zip(self.x, self.y):
            if i**2 + j**2 < 1:
                li[0].append(i)
                li[1].append(j)
            else:
                li[2].append(i)
                li[3].append(j)
        return li

    def show(self):
        print(len(self.x), len(self.y))
        if len(self.x) != len(self.y):
            raise Exception("Show : Bad array len")
        fig, ax = plt.subplots()
        circle = plt.Circle((0, 0), 1, fill=False,
                            edgecolor="red", linewidth=3)
        ax.add_artist(circle)
        a, b, c, d = self.__sep_point()
        ax.plot(a, b, 'ro')
        ax.plot(c, d, 'bo')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        plt.show()

    def __animate_step(self, frame):
        i, j = (self.x_cp.pop(0), self.y_cp.pop(0))
        if i**2 + j**2 < 1:
            self.a.append(i)
            self.b.append(j)
        else:
            self.c.append(i)
            self.d.append(j)
        im = []
        im += self.ax.plot(self.a, self.b, 'ro')
        im += self.ax.plot(self.c, self.d, 'bo')
        return im


    def animate(self, speed):
        self.x_cp = self.x[:]
        self.y_cp = self.y[:]
        self.a = []
        self.b = []
        self.c = []
        self.d = []
        fig, self.ax = plt.subplots()
        circle = plt.Circle((0, 0), 1, fill=False,
                            edgecolor="red", linewidth=3)
        self.ax.add_artist(circle)
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        ani = animation.FuncAnimation(fig, self.__animate_step, frames=range(5), interval=100/speed, blit=True)
        plt.show()


win = Viewer()


def my_random(a: int, b: int) -> float:
    """
    Generate a random float number between a and b.

    Parameters
    ----------
    a : int
        The minimum value of the random number range.
    b : int
        The maximum value of the random number range.

    Returns
    -------
    float
        A random float number between a and b.
    """
    rng = random.uniform(a, b)
    win.append(rng)
    return rng



def display_round(view: Viewer = win, speed: int = 1, mode: str = "animate") -> None:
    """
    Display the round using the specified mode.

    Parameters
    ----------
    speed : int, optional
        The speed of the animation, by default 1.
    mode : str, optional
        The mode to use to display the round, either "animate" or "show", by default "animate".

    Raises
    ------
    Exception
        If an invalid mode is specified.

    Returns
    -------
    None
    """
    if mode == "animate":
        view.animate(speed)
    elif mode == "show":
        view.show()
    else:
        raise Exception("display_round : Bad mode")


if __name__ == "__main__":
    with open("help.txt", "r") as f:
        print(f.read())
