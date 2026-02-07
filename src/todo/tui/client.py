from curses import curs_set, window, wrapper
from logging import DEBUG, Logger, getLogger

from .constants import Action
from .item import Item
from .windows import WinBase, WinItems
from todo.database import DatabaseClient
from todo.utils import terminal_height, terminal_width


class TUI:
    def __init__(
        self,
        database_client: DatabaseClient,
        logger: Logger = getLogger(__name__),
    ) -> None:
        self._logger = logger
        # TODO: Handle Resize
        self.database_client: DatabaseClient = database_client
        self.refresh_items()
        self.refresh_bounds()
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
        return self._database_client

    @database_client.setter
    def database_client(self, value: DatabaseClient) -> None:
        self._log(DEBUG, "Setting database client")
        self._database_client: DatabaseClient = value

    @property
    def items(self) -> list[Item]:
        return self._items

    @items.setter
    def items(self, value: list[Item]) -> None:
        self._log(DEBUG, f"Setting items to {value}")
        self._items: list[Item] = value

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
    def keep_running(self) -> bool:
        return self._keep_running

    @keep_running.setter
    def keep_running(self, value: bool) -> None:
        self._log(DEBUG, f"Setting keep_running to {value}")
        self._keep_running: bool = value

    @property
    def active_window(self) -> WinBase:
        return self._active_window

    @active_window.setter
    def active_window(self, value: WinBase) -> None:
        self._log(DEBUG, "Setting active window")
        self._active_window: WinBase = value

    @staticmethod
    def _message(message: str) -> str:
        return f"TUI: {message}"

    def _log(self, level: int, message: str) -> None:
        self._logger.log(level, self._message(message))

    def refresh_max_width(self) -> None:
        self.max_width = terminal_width() - 1

    def refresh_max_height(self) -> None:
        self.max_height = terminal_height()

    def refresh_bounds(self) -> None:
        self.refresh_max_width()
        self.refresh_max_height()

    def refresh_items(self) -> None:
        self._log(DEBUG, "Refreshing items")
        self.items: list[Item] = []
        for item in self.database_client.get_list()[1:]:
            self.items.append(Item(*item))

    def handle_input(self) -> None:
        key: int = self.active_window.getch()
        if key not in self.active_window.BINDINGS:
            return
        action: Action = self.active_window.BINDINGS[key]
        if action is Action.QUIT:
            self.keep_running = False
            # TODO: Handle nesting quits
        self.active_window.action(action)

    def main(self, stdscr: window) -> None:
        """
        Main Processing Loop For TUI

        Args:
            stdscr (window): curses window to display on
        """
        curs_set(0)
        win_items: WinItems = WinItems(
            width=self.max_width,
            height=self.max_height,
            items=self.items,
            logger=self._logger,
        )
        self.active_window = win_items
        # TODO: Handle stack
        stdscr.refresh()
        self.keep_running = True
        while self.keep_running:
            stdscr.clear()
            self.active_window.draw()
            self.handle_input()
