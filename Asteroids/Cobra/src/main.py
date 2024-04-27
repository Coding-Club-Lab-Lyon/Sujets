import Wrapper
from Vector2D import Vector2D

def is_str_overloaded(cls: type) -> bool:
    return cls.__str__ is not object.__str__


def main() -> None:
    """
    Entry point of the program.
    :return:
    """
    assert is_str_overloaded(Vector2D), "Le vecteur n'est pas encore réparé"
    wrapper = Wrapper.Wrapper(1920, 1080)
    wrapper.run()


if __name__ == "__main__":
    main()
