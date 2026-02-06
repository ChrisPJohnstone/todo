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

    @staticmethod
    def _message(message: str) -> str:
        return f"TUI: {message}"

    def _log(self, level: int, message: str) -> None:
        self._logger.log(level, self._message(message))

    def _draw_screen(self, win: window) -> None:
        win.addstr("Press q to quit")

    def main(self, stdscr: window) -> None:
        """
        Main Processing Loop For TUI

        Args:
            stdscr (window): curses window to display on
        """
        while True:
            stdscr.clear()
            self._draw_screen(stdscr)
            match stdscr.getkey():
                case "q":
                    break
            stdscr.refresh()
