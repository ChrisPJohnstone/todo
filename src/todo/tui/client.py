from curses import A_REVERSE, window, wrapper
from logging import DEBUG, Logger, getLogger

from todo.database import DatabaseClient
from todo.utils import terminal_width
from .constants import Action, BINDING
from .item import Item


class TUI:
    def __init__(
        self,
        database_client: DatabaseClient,
        logger: Logger = getLogger(__name__),
    ) -> None:
        self._logger = logger
        self.database_client: DatabaseClient = database_client
        self.refresh_items()
        wrapper(self.main)

    @property
    def _logger(self) -> Logger:
        return self.__logger

    @_logger.setter
    def _logger(self, value: Logger) -> None:
        self.__logger: Logger = value

    @property
    def database_client(self) -> DatabaseClient:
        """Database client used by TUI"""
        self._log(DEBUG, "Setting database client")
        return self._database_client

    @database_client.setter
    def database_client(self, value: DatabaseClient) -> None:
        self._database_client: DatabaseClient = value

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
    def max_index(self) -> int:
        return self.n_items - 1

    @property
    def max_id(self) -> int:
        return max([item.id for item in self.items])

    @property
    def max_id_len(self) -> int:
        return len(str(self.max_id))

    @property
    def current_index(self) -> int:
        return self._current_index

    @current_index.setter
    def current_index(self, value: int) -> None:
        self._log(DEBUG, f"Setting current index to {value}")
        if value < 0 or value > self.max_index:
            value = value % self.n_items
        self._current_index: int = value

    @property
    def current_item(self) -> Item:
        return self.items[self.current_index]

    @property
    def keep_running(self) -> bool:
        return self._keep_running

    @keep_running.setter
    def keep_running(self, value: bool) -> None:
        self._log(DEBUG, f"Setting keep_running to {value}")
        self._keep_running: bool = value

    @staticmethod
    def _message(message: str) -> str:
        return f"TUI: {message}"

    def _log(self, level: int, message: str) -> None:
        self._logger.log(level, self._message(message))

    def max_width(self) -> int:
        # TODO: Handle resize
        return terminal_width() - 1

    def refresh_items(self) -> None:
        self._log(DEBUG, "Refreshing items")
        self.items: list[Item] = []
        for item in self.database_client.get_list()[1:]:
            self.items.append(Item(*item))
        self.current_index = 0

    def draw_items(self, win: window) -> None:
        win.addstr("Press q to quit\n")
        divider: str = ": "
        id_width: int = self.max_id_len
        max_message_width: int = self.max_width() - id_width - len(divider)
        for index, item in enumerate(self.items):
            if len(item.message) >= max_message_width:
                message_str: str = f"{item.message[: max_message_width - 3]}..."
            else:
                message_str: str = item.message
            item_str: str = f"{item.id:>0{id_width}}{divider}{message_str}\n"
            if index == self.current_index:
                win.addstr(item_str, A_REVERSE)
            else:
                win.addstr(item_str)

    def handle_input(self, win: window) -> None:
        key: int = win.getch()
        if key not in BINDING:
            return
        match BINDING[key]:
            case Action.QUIT:
                self.keep_running = False
            case Action.DOWN:
                self.current_index += 1
            case Action.UP:
                self.current_index -= 1

    def main(self, stdscr: window) -> None:
        """
        Main Processing Loop For TUI

        Args:
            stdscr (window): curses window to display on
        """
        self.keep_running = True
        while self.keep_running:
            stdscr.clear()
            self.draw_items(stdscr)
            self.handle_input(stdscr)
