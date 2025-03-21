from datetime import datetime
from os import getuid
from pwd import getpwuid
import logging

from crontab import CronItem, CronTab


class ScheduleService:
    def __init__(self, user: str = "") -> None:
        self.user = user

    @staticmethod
    def get_user() -> str:
        return getpwuid(getuid())[0]

    @property
    def user(self) -> str:
        return self._user

    @user.setter
    def user(self, value: str) -> None:
        self._user: str = value or self.get_user()

    @staticmethod
    def cron_expression(when: datetime) -> str:
        return f"{when.minute} {when.hour} {when.day} {when.month} *"

    def schedule(self, command: str, when: datetime) -> None:
        logging.debug(f"Scheduling {command} for {when} for {self.user}")
        with CronTab(user=self.user) as cron:
            job: CronItem = cron.new(command=command)
            job.setall(ScheduleService.cron_expression(when))

    def unschedule(self, command: str) -> None:
        logging.debug(f"Unscheduling {command} for {self.user}")
        with CronTab(user=self.user) as cron:
            cron.remove_all(command=command)
