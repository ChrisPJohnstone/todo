from enum import Enum, auto, unique


@unique
class Action(Enum):
    DOWN = auto()
    ENTER = auto()
    GOTO_END = auto()
    GOTO_TOP = auto()
    JUMP_DOWN = auto()
    JUMP_UP = auto()
    QUIT = auto()
    UP = auto()
