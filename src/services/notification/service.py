from collections.abc import Callable

from ._linux import _send_notification_linux
from constants import Platform
from utils import operating_system

type SendMethod = Callable[[str], None]


class NotificationService:
    SEND_METHODS: dict[Platform, SendMethod] = {
        Platform.LINUX: _send_notification_linux,
    }

    @property
    def operating_system(self) -> Platform:
        """User's operating system."""
        if not hasattr(self, "_operating_system"):
            self._operating_system: Platform = operating_system()
        return self._operating_system

    def send_nofification(self, message: str) -> None:
        self.SEND_METHODS[self.operating_system](message)
