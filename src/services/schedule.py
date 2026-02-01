from datetime import datetime
from time import time
import sched

from .notification import NotificationService


class ScheduleService:
    def __init__(
        self,
        notifier: NotificationService | None = None,
    ) -> None:
        self.notifier = notifier or NotificationService()
        self.scheduler = sched.scheduler(time)

    @property
    def scheduler(self) -> sched.scheduler:
        return self._scheduler

    @scheduler.setter
    def scheduler(self, value: sched.scheduler) -> None:
        self._scheduler: sched.scheduler = value

    @property
    def notifier(self) -> NotificationService:
        return self._notifier

    @notifier.setter
    def notifier(self, value: NotificationService) -> None:
        self._notifier: NotificationService = value

    def clear(self) -> None:
        """Clear all events from scheduler"""
        for event in self.scheduler.queue:
            self.scheduler.cancel(event)

    def add_notification(self, due: datetime, message: str) -> None:
        """
        Add a notification to the scheduler

        Args:
            due (datetime): Time for notification to send
            message (str): Message to show in notification
        """
        self.scheduler.enterabs(
            time=due.timestamp(),
            priority=1,
            action=self.notifier.send_notification,
            kwargs={"message": message},
        )

    def run(self, blocking: bool = True) -> None:
        """Run all events in scheduler"""
        self.scheduler.run(blocking)
