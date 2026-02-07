from typing import Final

from .action import Action
from .key import Key


BINDING: Final[dict[int, Action]] = {
    Key.ARROW_DOWN: Action.DOWN,
    Key.ARROW_UP: Action.UP,
    Key.END: Action.GOTO_END,
    Key.HOME: Action.GOTO_TOP,
    Key.L_G: Action.GOTO_TOP,
    Key.L_J: Action.DOWN,
    Key.L_K: Action.UP,
    Key.L_Q: Action.QUIT,
    Key.U_G: Action.GOTO_END,
}
