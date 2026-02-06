from enum import Enum, auto, unique


@unique
class Action(Enum):
    QUIT = auto()
    UP = auto()
    DOWN = auto()
