from typing import Final

from .action import Action
from .key import Key


BINDING: Final[dict[int, Action]] = {
    Key.ARROW_DOWN: Action.DOWN,
    Key.ARROW_UP: Action.UP,
    Key.L_J: Action.DOWN,
    Key.L_K: Action.UP,
    Key.L_Q: Action.QUIT,
}
