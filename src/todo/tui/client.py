from curses import window, wrapper
from logging import DEBUG, Logger, getLogger

from todo.database import DatabaseClient


class TUI:
    def __init__(
        self,
        database_client: DatabaseClient,
        logger: Logger = getLogger(__name__),
    ) -> None:
        self._logger = logger
        self.database_client: DatabaseClient = database_client
        self._refresh_items()
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
    def items(self) -> list[tuple]:
        return self._items

    @items.setter
    def items(self, value: list[tuple]) -> None:
        self._log(DEBUG, f"Setting items to {value}")
        self._items: list[tuple] = value

    @staticmethod
    def _message(message: str) -> str:
        return f"TUI: {message}"

    def _log(self, level: int, message: str) -> None:
        self._logger.log(level, self._message(message))

    def _refresh_items(self) -> None:
        self._log(DEBUG, "Refreshing items")
        self.items = self.database_client.get_list()

    def _draw_screen(self, win: window) -> None:
        win.addstr("Press q to quit\n")
        for item in self.items:
            row: str = " ".join([str(cell) for cell in item])
            win.addstr(f"{row}\n")

    def main(self, stdscr: window) -> None:
        """
        Main Processing Loop For TUI

        Args:
            stdscr (window): curses window to display on
        """
        stdscr.clear()
        self._draw_screen(stdscr)
        while True:
            match stdscr.getkey():
                case "q":
                    break
                case _:
                    continue
            stdscr.clear()
            self._draw_screen(stdscr)
            stdscr.refresh()
