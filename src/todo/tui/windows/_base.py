from abc import ABC, abstractmethod
from curses import newpad, window
from logging import DEBUG, Logger, getLogger

from ..constants import Action, BINDING


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
        self.keep_running = True

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

    @property
    def keep_running(self) -> bool:
        return self._keep_running

    @keep_running.setter
    def keep_running(self, value: bool) -> None:
        self._log(DEBUG, f"Setting keep_running to {value}")
        self._keep_running: bool = value

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

    @abstractmethod
    def _action(self, action: Action) -> None:
        pass

    def handle_input(self) -> None:
        key: int = self._win.getch()
        if key not in BINDING:
            return
        self._action(BINDING[key])
        # TODO: Handle bindings per window
