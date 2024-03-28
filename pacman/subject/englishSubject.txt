## Pacman:

![pacman.png](assets/pacman.png)
*Illustration by PixelOz*

The aim of this project is to create a simplified version of the famous game Pacman.

As you cannot build the game from scratch in 2 hours, I provide you with some wrapper code that will allow you to focus on the implementation of the game logic.<br>
The game will be rendered using Tkinter, but you will not directly interact with it.

## 1. Introduction:

### Prerequisites:

- [Python](https://www.python.org/downloads/) installed
- [Pip](https://pip.pypa.io/en/stable/installing/) installed
- [Tkinter](https://tkdocs.com/tutorial/install.html) installed

### Objectives:

- Discover the basics of Oriented Object Programming in Python
- Create / manipulate classes and objects
- Have fun

### Testing:

Since I manually removed parts of the code, running it will result in an error.<br>
You have 2 choices:
- Fix all the code, then when you are able to run it, debug it
- Modify the code to remove call to function you didn't fix yet, then fix them one by one

Either way are good, choose the one that suits you the best.

### Difficulty and communication:

The subject may seem not to give you many instructions, has it is your goal to make the needed research to understand the code and to implement the game logic.<br>
This project isn't an evaluation, you **have** to communicate with your classmates to finish the project.<br>
Keep in mind that this project is difficult by design, ask google, ask your classmates, ask us, but do not give up!

This project has 2 difficulty levels, take the one that suits you the best:

- **Normal**: You will have to implement some of the game logic alongside some library functions.
- **Hard**: You will have to implement the whole game logic from scratch.

**Good luck soldier!**

### 1.1. Variables and Types:

As you surely know, Python use a weakly typed system. This means that you do not have to declare the type of a variable before using it. The type of a variable is determined by the value you assign to it.<br>
However, it isn't a good practice to use this feature as this can lead to confusion and bugs. That's why I recommend you to always declare the type of your variables.<br>
To do so, you can use the following syntax:

```python
variable_name: type = value
```

For function, you can declare the type of the arguments and the return value like this:

```python
def function_name(arg1: type1, arg2: type2) -> return_type:
    pass
```

Even if Python will not enforce the type, it will help you to understand your code and to avoid mistakes.<br>
I highly recommend you to use this feature in this project.

!pagebreak

## 2. First steps:

To start the project, you will need to fix the `main.py` and `library.py` files.<br>
It will be a small introduction to the project and the code you will have to write.
Guidance will be provided in the functions' docstrings.

### 2.1. `main.py`:

This file is the entry point of the project. It will be used to start the game and to interact with the player.

### 2.2. `library.py`:

This file contains some generic functions that does not fit in classes.<br>
It also provide useful classes like `Vector2D` and `BadFileException`.

>:info If you are already familiar with Oriented Object Programming, you can skip this section.

#### 2.2.1. `Vector2D`:

This class represents a 2D vector. It will be used to represent the direction of the entities in the game.<br>

Since we are defining a custom type, we need to define operation on it.<br>
In Oriented Object Programming, this is called operator overloading.<br>
To achieve this in python, you can use the following syntax:

```python
def __add__(self, other: Vector2D) -> Vector2D:
    pass
```

#### 2.2.2. `BadFileException`:

This class is a custom exception.<br>
We use a custom exception to handle specific errors that can occur in our code.<br>

This class show us a new OOP concept: inheritance.<br>
Inheritance is a way to create a new class that reuse the properties and methods of an existing class.<br>
In python, you can inherit from a class like this:

```python
class ParentClass:
    pass

class ChildClass(ParentClass):
    pass
```

To truly use the parent class, you also need to call its constructor:

```python
class ChildClass(ParentClass):
    def __init__(self):
        super().__init__()
```

`super()` is a function that return the parent class of the current class.

>:warning Be sure to understand this part before moving on. Do not hesitate to ask questions if you are not sure.

!pagebreak

## 3. The game:

>:success This is where the fun begins!

Now that you have fixed the library and have a better understanding of OOP, you can start implementing the game logic.<br>

>:warning This part is more complex than the previous one. Do not hesitate to ask questions if you are not sure.

In this part, I provide you with 3 classes.

### 3.1. `SpriteHandler`:

As stated before, the aim of this project isn't for you to manipulate Tkinter.<br>
I encourage you to read the class (as I'm proud of it), but you will not have to modify it (it's already perfect!).

has the name suggests, this class will handle the sprites of the game.<br>

### 3.2. `Entity`:

This class represents an entity in the game.<br>
Apart from the boolean `is_player`, you have no way to know what kind of entity it is.<br>
This is the purpose of the `Entity` class: to be a generic class that can be used for any kind of entity.

To make it more readable, the player has a custom `move` method.<br>

## 4. Bonus:

>:success Congratulations on going this far!

But the fun doesn't stop here! You can add more features to the game.<br>

Here are some ideas:
- Add more entities (ghosts, fruits, ...)
- Add a lives system
- Add a menu

This are some 'gameplay' ideas, but you can also improve the code:

### 4.1. map representation:

Currently, the game is only represented by a 2D list, which is easy, but janky.<br>
To address this, here are two ideas:
- Create a `Map` class that will handle the map representation
- Strip away the 'map' logic and use Vector2D to represent the entities' position

### 4.2. AI:

The current 'AI' of the ghost(s) is very basic and rely on a random.<br>
Feel free to add a real AI to the ghost(s)!<br>
To achive this, here some ideas:
- When a ghost see the player, it will follow him (simple, but effective)
- Implement a pathfinding algorithm that will track the player (hard, but rewarding)

Speaking of pathfinding, here are some algorithms you can use:
- A* (A-star)
- Dijkstra
- Breadth-first search
- Depth-first search

I personally recommend A* as it is the most efficient and the easiest to implement, but all of them are good choices with pros and cons.

**Enough reading, go have fun!**

## 5. Glossary:

- **Wrapper**: A piece of code that provides a simplified interface to a more complex library or code set.
- **OOP**: Oriented Object Programming
- **Inheritance**: A way to create a new class that reuse the properties and methods of an existing class.
- **Operator overloading**: A way to define a custom behavior for an operator (like `+`, `-`, `*`, ...).
