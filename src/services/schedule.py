from datetime import datetime
from os import fork
from time import time
import sched

from .notification import NotificationService


class ScheduleService:
    def __init__(self) -> None:
        self.scheduler = sched.scheduler(time)
        # TODO: Handle persistence of scheduled tasks
        # TODO: Handle stopping scheduled tasks if due modified

    @property
    def scheduler(self) -> sched.scheduler:
        return self._scheduler

    @scheduler.setter
    def scheduler(self, value: sched.scheduler) -> None:
        self._scheduler: sched.scheduler = value

    @property
    def notifier(self) -> NotificationService:
        if not hasattr(self, "_notifier"):
            self._notifier: NotificationService = NotificationService()
        return self._notifier

    def schedule_notification(self, due: datetime, message: str) -> None:
        self.scheduler.enterabs(
            time=due.timestamp(),
            priority=1,
            action=self.notifier.send_notification,
            kwargs={"message": message},
        )
        child_pid: int = fork()
        if child_pid != 0:
            return
        self.scheduler.run()
