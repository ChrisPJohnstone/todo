from typing import Final

from ._linux import _send_notification_linux
from ._mac import _send_notification_mac
from todo.constants import Platform
from todo.utils import operating_system


class NotificationClient:
    DEFAULT_APP_NAME: Final[str] = "todo"
    DEFAULT_EXPIRY_TIME: Final[int] = 3

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

    def send_notification(self, message: str) -> None:
        """
        Send a notification to the user.

        Args:
            message (str): The message to be sent in the notification.
        """
        match self.operating_system:
            case Platform.MAC:
                _send_notification_mac(
                    title=self.app_name,
                    message=message,
                )
            case Platform.LINUX:
                _send_notification_linux(
                    app_name=self.app_name,
                    expiry_time=self.expiry_time,
                    message=message,
                )
            case _:
                raise NotImplementedError(
                    f"Notifications not supported on {self.operating_system}"
                )
