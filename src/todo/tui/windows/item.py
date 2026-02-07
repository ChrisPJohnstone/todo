from curses import newwin, window
from logging import DEBUG, Logger, getLogger

from ..constants import Action, Key
from ..item import Item
from ..type_definitions import Bindings
from ._base import WinBase


class WinItem(WinBase):
    def __init__(
        self,
        x_max: int,
        y_max: int,
        x_len_max: int,
        y_len_max: int,
        item: Item,
        x_strt: int = 0,
        y_strt: int = 0,
        logger: Logger = getLogger(__name__),
    ) -> None:
        super().__init__(
            x_strt=x_strt,
            y_strt=y_strt,
            x_max=x_max,
            y_max=y_max,
            x_len_max=x_len_max,
            y_len_max=y_len_max,
            logger=logger,
        )
        self.item = item

    @property
    def BINDINGS(self) -> Bindings:
        return {
            Key.L_Q: Action.QUIT,
        }

    @property
    def item(self) -> Item:
        return self._items

    @item.setter
    def item(self, value: Item) -> None:
        self._log(DEBUG, f"Setting item to {value}")
        self._items: Item = value
        self.index_current = 0

    @staticmethod
    def _message(message: str) -> str:
        return f"Item Window: {message}"

    def init_win(self) -> None:
        self._win = newwin(
            self.y_len,  # nlines
            self.x_len,  # ncols
            self.y_strt,  # begin_y
            self.x_strt,  # begin_x
        )

    def _draw(self) -> None:
        self._log(DEBUG, "Drawing")
        self._win.vline(self.y_strt, self.x_strt)
        self._win.refresh()
        message_win: window = newwin(
            self.y_len,  # nlines
            self.x_len - 1,  # ncols
            self.y_strt,  # begin_y
            self.x_strt + 1,  # begin_x
        )
        message_win.addstr(0, 0, self.item.message)
        message_win.refresh()

    def action(self, action: Action, windows: list[WinBase]) -> None:
        match action:
            case Action.QUIT:
                windows.pop(0)
