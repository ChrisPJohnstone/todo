from curses import A_REVERSE, newwin
from logging import DEBUG, Logger, getLogger

from ..constants import Action, Key
from ..item import Item
from ..type_definitions import Bindings
from ._base import WinBase
from .item import WinItem
from todo.database import DatabaseClient


class WinItems(WinBase):
    def __init__(
        self,
        database_client: DatabaseClient,
        x_max: int,
        y_max: int,
        x_len_max: int,
        y_len_max: int,
        x_strt: int = 0,
        y_strt: int = 0,
        logger: Logger = getLogger(__name__),
    ) -> None:
        super().__init__(
            database_client=database_client,
            x_strt=x_strt,
            y_strt=y_strt,
            x_max=x_max,
            y_max=y_max,
            x_len_max=x_len_max,
            y_len_max=y_len_max,
            logger=logger,
        )
        self.refresh_items()

    @property
    def BINDINGS(self) -> Bindings:
        return {
            Key.ARROW_DOWN: Action.DOWN,
            Key.ARROW_UP: Action.UP,
            Key.CTRL_M: Action.ENTER,
            Key.CTRL_J: Action.ENTER,
            Key.END: Action.GOTO_END,
            Key.ENTER: Action.ENTER,
            Key.HOME: Action.GOTO_TOP,
            Key.L_D: Action.JUMP_DOWN,
            Key.L_G: Action.GOTO_TOP,
            Key.L_J: Action.DOWN,
            Key.L_K: Action.UP,
            Key.L_Q: Action.QUIT,
            Key.L_U: Action.JUMP_UP,
            Key.U_G: Action.GOTO_END,
        }

    @property
    def items(self) -> list[Item]:
        return self._items

    @items.setter
    def items(self, value: list[Item]) -> None:
        self._log(DEBUG, f"Setting items to {value}")
        self._items: list[Item] = value
        self.index_current = 0

    @property
    def n_items(self) -> int:
        return len(self.items)

    @property
    def index_max(self) -> int:
        return self.n_items - 1

    @property
    def max_id(self) -> int:
        return max([item.id for item in self.items])

    @property
    def max_id_len(self) -> int:
        return len(str(self.max_id))

    @property
    def index_current(self) -> int:
        return self._current_index

    @index_current.setter
    def index_current(self, value: int) -> None:
        self._log(DEBUG, f"Setting current index to {value}")
        if value < 0 or value > self.index_max:
            self._log(DEBUG, "Wrapping out of bounds value")
            value = value % self.n_items
        self._current_index: int = value
        self.refresh_page_start()

    @property
    def index_start(self) -> int:
        return self._index_start

    @index_start.setter
    def index_start(self, value: int) -> None:
        self._log(DEBUG, f"Setting index_start to {value}")
        self._index_start: int = value

    @property
    def index_end(self) -> int:
        return self.index_start + min(self.n_items, self.y_len)

    @staticmethod
    def _message(message: str) -> str:
        return f"Items Window: {message}"

    def init_win(self) -> None:
        self._win = newwin(
            self.y_len,  # nlines
            self.x_len,  # ncols
            self.y_strt,  # begin_y
            self.x_strt,  # begin_x
        )

    def refresh_items(self) -> None:
        self._log(DEBUG, "Refreshing items")
        self.items = [
            Item(*item) for item in self.database_client.get_list()[1:]
        ]

    def refresh_page_start(self) -> None:
        self._log(DEBUG, "Redrawing bounds")
        if not hasattr(self, "_index_start"):
            self.index_start = 0
        if self.index_current < self.index_start:
            self._log(DEBUG, "Moving page up")
            self.index_start = self.index_current
        if self.index_current > self.index_end - 1:
            self._log(DEBUG, "Moving page down")
            relative_position: int = self.index_current - self.index_start
            self.index_start += relative_position - self.y_len + 1

    def _draw(self) -> None:
        self._log(DEBUG, "Drawing")
        divider: str = ": "
        id_width: int = self.max_id_len
        max_message_width: int = self.x_len - id_width - len(divider)
        line: int = 0
        for index in range(self.index_start, self.index_end):
            item: Item = self.items[index]
            if len(item.message) > max_message_width:
                message_str: str = f"{item.message[: max_message_width - 3]}..."
            else:
                message_str: str = item.message
            item_str: str = f"{item.id:>0{id_width}}{divider}{message_str}"
            if index == self.index_current:
                self._win.addstr(line, 0, item_str, A_REVERSE)
            else:
                self._win.addstr(line, 0, item_str)
            line += 1
        self._win.refresh()

    def action(self, action: Action, windows: list[WinBase]) -> None:
        match action:
            case Action.QUIT:
                windows.pop(0)
            case Action.DOWN:
                self.index_current += 1
            case Action.UP:
                self.index_current -= 1
            case Action.GOTO_TOP:
                self.index_current = 0
            case Action.GOTO_END:
                self.index_current = self.index_max
            case Action.JUMP_DOWN:
                new: int = self.index_current + (self.y_len_max // 2)
                self.index_current = min(new, self.index_max)
            case Action.JUMP_UP:
                new: int = self.index_current - (self.y_len_max // 2)
                self.index_current = max(new, 0)
            case Action.ENTER:
                win_item: WinItem = WinItem(
                    database_client=self.database_client,
                    x_strt=self.x_len_max // 2,
                    y_strt=self.y_strt,
                    x_max=self.x_max,
                    y_max=self.y_max,
                    x_len_max=self.x_len_max,
                    y_len_max=self.y_len_max,
                    item=self.items[self.index_current],
                    logger=self._logger,
                )
                windows.insert(0, win_item)
