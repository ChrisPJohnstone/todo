from curses import curs_set, window, wrapper
from logging import DEBUG, Logger, getLogger

from .constants import Action
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
    def cols(self) -> int:
        return self._cols

    @cols.setter
    def cols(self, value: int) -> None:
        self._log(DEBUG, f"Setting max width to {value}")
        self._cols: int = value

    @property
    def rows(self) -> int:
        return self._rows

    @rows.setter
    def rows(self, value: int) -> None:
        self._log(DEBUG, f"Setting max height to {value}")
        self._rows: int = value

    @property
    def windows(self) -> list[WinBase]:
        return self._windows

    @windows.setter
    def windows(self, value: list[WinBase]) -> None:
        self._log(DEBUG, f"Settings windows to {value}")
        self._windows: list[WinBase] = value

    @property
    def active_window(self) -> WinBase:
        return self.windows[0]

    @staticmethod
    def _message(message: str) -> str:
        return f"TUI: {message}"

    def _log(self, level: int, message: str) -> None:
        self._logger.log(level, self._message(message))

    def refresh_cols(self) -> None:
        self.cols = terminal_width() - 1

    def refresh_rows(self) -> None:
        self.rows = terminal_height()

    def refresh_bounds(self) -> None:
        self.refresh_cols()
        self.refresh_rows()

    def handle_input(self) -> None:
        key: int = self.active_window.getch()
        self._log(DEBUG, f"Key {key} pressed")
        if key not in self.active_window.BINDINGS:
            return
        action: Action = self.active_window.BINDINGS[key]
        self.active_window.action(action, self.windows)

    def main(self, stdscr: window) -> None:
        """
        Main Processing Loop For TUI

        Args:
            stdscr (window): curses window to display on
        """
        curs_set(0)
        win_items: WinItems = WinItems(
            database_client=self.database_client,
            x_max=self.cols,
            y_max=self.rows,
            x_len_max=self.cols,
            y_len_max=self.rows,
            logger=self._logger,
        )
        self.windows = [win_items]
        stdscr.refresh()
        while self.windows:
            self.active_window.draw()
            self.handle_input()
