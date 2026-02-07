from curses import A_REVERSE
from logging import DEBUG, Logger, getLogger

from ._base import WinBase
from ..constants import Action
from ..item import Item


class WinItems(WinBase):
    def __init__(
        self,
        width: int,
        height: int,
        items: list[Item],
        logger: Logger = getLogger(__name__),
    ) -> None:
        super().__init__(width, height, logger)
        self.items = items

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
        return self.index_start + min(self.n_items, self.height)

    @staticmethod
    def _message(message: str) -> str:
        return f"Items Window: {message}"

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
            self.index_start += relative_position - self.height + 1

    def _draw(self) -> None:
        self._log(DEBUG, "test")
        divider: str = ": "
        id_width: int = self.max_id_len
        max_message_width: int = self.width - id_width - len(divider)
        line: int = 0
        for index in range(self.index_start, self.index_end):
            item: Item = self.items[index]
            if len(item.message) >= max_message_width:
                message_str: str = f"{item.message[: max_message_width - 3]}..."
            else:
                message_str: str = item.message
            item_str: str = f"{item.id:>0{id_width}}{divider}{message_str}"
            if index == self.index_current:
                self._win.addstr(line, 0, item_str, A_REVERSE)
            else:
                self._win.addstr(line, 0, item_str)
            line += 1
        self._win.refresh(0, 0, 0, 0, self.height - 1, self.width)

    def _action(self, action: Action) -> None:
        match action:
            case Action.QUIT:
                self.keep_running = False
            case Action.DOWN:
                self.index_current += 1
            case Action.UP:
                self.index_current -= 1
            case Action.GOTO_TOP:
                self.index_current = 0
            case Action.GOTO_END:
                self.index_current = self.index_max
            case Action.JUMP_DOWN:
                new: int = self.index_current + (self.height // 2)
                self.index_current = min(new, self.index_max)
            case Action.JUMP_UP:
                new: int = self.index_current - (self.height // 2)
                self.index_current = max(new, 0)
