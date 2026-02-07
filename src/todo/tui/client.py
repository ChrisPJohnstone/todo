from curses import curs_set, window, wrapper
from logging import DEBUG, Logger, getLogger

from .windows import WinItems
from todo.database import DatabaseClient
from todo.utils import terminal_height, terminal_width


class TUI:
    def __init__(
        self,
        database_client: DatabaseClient,
        logger: Logger = getLogger(__name__),
    ) -> None:
        self._logger = logger
        self.database_client: DatabaseClient = database_client
        self.refresh_bounds()
        # TODO: Handle Resize
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

    def main(self, stdscr: window) -> None:
        """
        Main Processing Loop For TUI

        Args:
            stdscr (window): curses window to display on
        """
        curs_set(0)
        win_items: WinItems = WinItems(
            max_width=self.max_width,
            max_height=self.max_height,
            database_client=self.database_client,
            logger=self._logger,
        )
        stdscr.refresh()
        while win_items.keep_running:
            stdscr.clear()
            win_items.draw_items(stdscr)
            win_items.handle_input(stdscr)
