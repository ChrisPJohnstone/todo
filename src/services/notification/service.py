from collections.abc import Callable
from typing import Final

from ._linux import _send_notification_linux
from constants import Platform
from utils import operating_system

type SendMethod = Callable[[str, int, str], None]


class NotificationService:
    DEFAULT_APP_NAME: Final[str] = "todo"
    DEFAULT_EXPIRY_TIME: Final[int] = 3
    SEND_METHODS: Final[dict[Platform, SendMethod]] = {
        Platform.LINUX: _send_notification_linux,
    }

    def __init__(
        self,
        app_name: str = DEFAULT_APP_NAME,
        expiry_time: int = DEFAULT_EXPIRY_TIME,
    ) -> None:
        self.app_name = app_name
        self.expiry_time = expiry_time

    @property
    def app_name(self) -> str:
        """Application name for the notification."""
        return self._app_name

    @app_name.setter
    def app_name(self, value: str) -> None:
        self._app_name: str = value

    @property
    def expiry_time(self) -> int:
        """Expiry time for the notification in seconds."""
        return self._expiry_time

    @expiry_time.setter
    def expiry_time(self, value: int) -> None:
        self._expiry_time: int = value

    @property
    def operating_system(self) -> Platform:
        """User's operating system."""
        if not hasattr(self, "_operating_system"):
            self._operating_system: Platform = operating_system()
        return self._operating_system

    def send_nofification(self, message: str) -> None:
        self.SEND_METHODS[self.operating_system](
            self.app_name,
            self.expiry_time,
            message,
        )
