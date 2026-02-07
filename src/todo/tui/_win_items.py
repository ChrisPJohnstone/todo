from curses import A_REVERSE, newpad, window
from logging import DEBUG, Logger, getLogger

from todo.database import DatabaseClient
from .constants import Action, BINDING
from .item import Item


class WinItems:
    def __init__(
        self,
        max_width: int,
        max_height: int,
        database_client: DatabaseClient,
        logger: Logger = getLogger(__name__),
    ) -> None:
        self._logger = logger
        self._win = newpad(1000, 1000)
        # TODO: Fix hardcoded
        self.max_width = max_width
        self.max_height = max_height
        self.keep_running = True
        self.database_client: DatabaseClient = database_client
        self.refresh_items()

    @property
    def _logger(self) -> Logger:
        return self.__logger

    @_logger.setter
    def _logger(self, value: Logger) -> None:
        self.__logger: Logger = value

    @property
    def _win(self) -> window:
        return self.__win

    @_win.setter
    def _win(self, value: window) -> None:
        self._log(DEBUG, "Setting _win")
        self.__win: window = value

    @property
    def database_client(self) -> DatabaseClient:
        """Database client used by TUI"""
        return self._database_client

    @database_client.setter
    def database_client(self, value: DatabaseClient) -> None:
        self._log(DEBUG, "Setting database client")
        self._database_client: DatabaseClient = value

    @property
    def keep_running(self) -> bool:
        return self._keep_running

    @keep_running.setter
    def keep_running(self, value: bool) -> None:
        self._log(DEBUG, f"Setting keep_running to {value}")
        self._keep_running: bool = value

    @property
    def max_width(self) -> int:
        return self._max_width

    @max_width.setter
    def max_width(self, value: int) -> None:
        self._log(DEBUG, f"Setting max width to {value}")
        self._max_width: int = value

    @property
    def max_height(self) -> int:
        return self._max_height

    @max_height.setter
    def max_height(self, value: int) -> None:
        self._log(DEBUG, f"Setting max height to {value}")
        self._max_height: int = value

    @property
    def items(self) -> list[Item]:
        return self._items

    @items.setter
    def items(self, value: list[Item]) -> None:
        self._log(DEBUG, f"Setting items to {value}")
        self._items: list[Item] = value

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
        return self.index_start + min(self.n_items, self.max_height)

    @staticmethod
    def _message(message: str) -> str:
        return f"Items Window: {message}"

    def _log(self, level: int, message: str) -> None:
        self._logger.log(level, self._message(message))

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
            self.index_start += relative_position - self.max_height + 1

    def refresh_items(self) -> None:
        self._log(DEBUG, "Refreshing items")
        self.items: list[Item] = []
        for item in self.database_client.get_list()[1:]:
            self.items.append(Item(*item))
        self.index_current = 0

    def draw_items(self, win: window) -> None:
        self._log(DEBUG, "test")
        divider: str = ": "
        id_width: int = self.max_id_len
        max_message_width: int = self.max_width - id_width - len(divider)
        line: int = 0
        for index in range(self.index_start, self.index_end):
            item: Item = self.items[index]
            if len(item.message) >= max_message_width:
                message_str: str = f"{item.message[: max_message_width - 3]}..."
            else:
                message_str: str = item.message
            item_str: str = f"{item.id:>0{id_width}}{divider}{message_str}"
            if index == self.index_current:
                win.addstr(line, 0, item_str, A_REVERSE)
            else:
                win.addstr(line, 0, item_str)
            line += 1
        self._win.refresh(0, 0, 0, 0, self.max_height - 1, self.max_width)

    def handle_input(self, win: window) -> None:
        key: int = win.getch()
        if key not in BINDING:
            return
        match BINDING[key]:
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
                new: int = self.index_current + (self.max_height // 2)
                self.index_current = min(new, self.index_max)
            case Action.JUMP_UP:
                new: int = self.index_current - (self.max_height // 2)
                self.index_current = max(new, 0)
