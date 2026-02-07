from __future__ import annotations  # TODO: Remove at 3.14+
from abc import ABC, abstractmethod
from curses import window
from logging import DEBUG, Logger, getLogger

from ..constants import Action
from ..type_definitions import Bindings
from todo.database import DatabaseClient
from todo.utils import terminal_height, terminal_width


class WinBase(ABC):
    def __init__(
        self,
        database_client: DatabaseClient,
        x_strt: int = 0,
        y_strt: int = 0,
        x_len_max: int = 0,
        y_len_max: int = 0,
        logger: Logger = getLogger(__name__),
    ) -> None:
        self._logger = logger
        self.database_client: DatabaseClient = database_client
        self.refresh_bounds()
        self.x_strt = x_strt
        self.y_strt = y_strt
        self.x_len_max = x_len_max
        self.y_len_max = y_len_max
        self.init_win()

    @property
    @abstractmethod
    def BINDINGS(self) -> Bindings:
        pass

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
    def x_max(self) -> int:
        return self._x_max

    @x_max.setter
    def x_max(self, value: int) -> None:
        self._log(DEBUG, f"Setting x_max to {value}")
        self._x_max: int = value

    @property
    def y_max(self) -> int:
        return self._y_max

    @y_max.setter
    def y_max(self, value: int) -> None:
        self._log(DEBUG, f"Setting y_max to {value}")
        self._y_max: int = value

    @property
    def x_strt(self) -> int:
        return self._x_strt

    @x_strt.setter
    def x_strt(self, value: int) -> None:
        self._log(DEBUG, f"Setting x_strt to {value}")
        self._x_strt: int = value

    @property
    def x_len_max(self) -> int:
        return self._x_len_max

    @x_len_max.setter
    def x_len_max(self, value: int) -> None:
        self._log(DEBUG, f"Setting x_len_max to {value}")
        if value == 0:
            value = self.x_max
        self._x_len_max: int = value

    @property
    def x_stop(self) -> int:
        return min(self.x_max, self.x_strt + self.x_len_max)

    @property
    def x_len(self) -> int:
        return self.x_stop - self.x_strt + 1

    @property
    def y_strt(self) -> int:
        return self._y_strt

    @y_strt.setter
    def y_strt(self, value: int) -> None:
        self._log(DEBUG, f"Setting y_strt to {value}")
        self._y_strt: int = value

    @property
    def y_len_max(self) -> int:
        return self._y_len_max

    @y_len_max.setter
    def y_len_max(self, value: int) -> None:
        self._log(DEBUG, f"Setting y_len_max to {value}")
        if value == 0:
            value = self.y_max
        self._y_len_max: int = value

    @property
    def y_stop(self) -> int:
        return min(self.y_max, self.y_strt + self.y_len_max)

    @property
    def y_len(self) -> int:
        return self.y_stop - self.y_strt

    @staticmethod
    @abstractmethod
    def _message(message: str) -> str:
        pass

    def _log(self, level: int, message: str) -> None:
        self._logger.log(level, self._message(message))

    def refresh_cols(self) -> None:
        self.x_max = terminal_width() - 1

    def refresh_rows(self) -> None:
        self.y_max = terminal_height()

    def refresh_bounds(self) -> None:
        self.refresh_cols()
        self.refresh_rows()

    @abstractmethod
    def init_win(self) -> None:
        pass

    @abstractmethod
    def _draw(self) -> None:
        pass

    def draw(self) -> None:
        self._win.clear()
        self._draw()

    def getch(self) -> int:
        return self._win.getch()

    @abstractmethod
    def action(self, action: Action, windows: list[WinBase]) -> None:
        pass
