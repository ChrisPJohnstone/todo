from curses import window, wrapper
from logging import DEBUG, Logger, getLogger

from todo.database import DatabaseClient
from todo.utils import terminal_width
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

    @staticmethod
    def _message(message: str) -> str:
        return f"TUI: {message}"

    def _log(self, level: int, message: str) -> None:
        self._logger.log(level, self._message(message))

    def max_id(self) -> int:
        return max([item.id for item in self.items])

    def id_width(self) -> int:
        return len(str(self.max_id()))

    def max_width(self) -> int:
        # TODO: Handle resize
        return terminal_width() - 1

    def refresh_items(self) -> None:
        self._log(DEBUG, "Refreshing items")
        self.items: list[Item] = []
        for item in self.database_client.get_list()[1:]:
            self.items.append(Item(*item))

    def draw_items(self, win: window) -> None:
        win.addstr("Press q to quit\n")
        divider: str = ": "
        id_width: int = self.id_width()
        max_message_width: int = self.max_width() - id_width - len(divider)
        for item in self.items:
            if len(item.message) >= max_message_width:
                message_str: str = f"{item.message[: max_message_width - 3]}..."
            else:
                message_str: str = item.message
            win.addstr(f"{item.id:>0{id_width}}{divider}{message_str}\n")

    def main(self, stdscr: window) -> None:
        """
        Main Processing Loop For TUI

        Args:
            stdscr (window): curses window to display on
        """
        stdscr.clear()
        self.draw_items(stdscr)
        while True:
            match stdscr.getkey():
                case "q":
                    break
                case _:
                    continue
            stdscr.clear()
            self.draw_items(stdscr)
            stdscr.refresh()
