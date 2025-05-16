from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from datetime import datetime
from os import getenv

from src.services import ScheduleService


class Command(ABC):
    @staticmethod
    @abstractmethod
    def parent_parsers() -> list[ArgumentParser]:
        pass

    @abstractmethod
    def __init__(self, args: Namespace) -> None:
        pass

    @staticmethod
    def notification_command(item_id: int) -> str:
        return f"send-notification `td show {item_id}`"

    @staticmethod
    def schedule_notification(item_id: int, due: datetime) -> None:
        command: str = (
            f"export PATH={getenv('PATH')} ; "
            f"{Command.notification_command(item_id)}"
        )
        # TODO: Figure out a better way to manage path
        ScheduleService().schedule(command=command, when=due)

    @staticmethod
    def unschedule_notification(item_id: int) -> None:
        command: str = Command.notification_command(item_id)
        ScheduleService().unschedule(command=command)
