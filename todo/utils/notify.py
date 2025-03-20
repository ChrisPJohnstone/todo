from notifypy import Notify


class Notifier:
    def __init__(
        self,
        title: str = "",
        application_name: str = "",
    ) -> None:
        self.title = title
        self.application_name = application_name

    @property
    def DEFAULT_TITLE(self) -> str:
        return "TODO"

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title: str = value or self.DEFAULT_TITLE

    @property
    def DEFAULT_APPLICATION_NAME(self) -> str:
        return "TODO"

    @property
    def application_name(self) -> str:
        return self._application_name

    @application_name.setter
    def application_name(self, value: str) -> None:
        self._application_name: str = value or self.DEFAULT_APPLICATION_NAME

    def send(self, message: str) -> None:
        Notify(
            default_notification_title=self.title,
            default_notification_message=message,
            default_notification_application_name=self.application_name,
        ).send()
