from __future__ import annotations  # TODO: Remove at 3.14+
from abc import ABC, abstractmethod
from curses import newpad, window
from logging import DEBUG, Logger, getLogger

from ..constants import Action
from ..type_definitions import Bindings


class WinBase(ABC):
    def __init__(
        self,
        width: int,
        height: int,
        logger: Logger = getLogger(__name__),
    ) -> None:
        self._logger = logger
        self._win = newpad(1000, 1000)
        # TODO: Give options to children
        # TODO: Fix hardcoded
        self.width = width
        self.height = height

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
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._log(DEBUG, f"Setting width to {value}")
        self._width: int = value

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._log(DEBUG, f"Setting height to {value}")
        self._height: int = value

    @staticmethod
    @abstractmethod
    def _message(message: str) -> str:
        pass

    def _log(self, level: int, message: str) -> None:
        self._logger.log(level, self._message(message))

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
