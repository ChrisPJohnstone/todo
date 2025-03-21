from abc import ABC, abstractmethod
from argparse import _SubParsersAction, ArgumentParser, Namespace
from datetime import datetime

from todo.services import ScheduleService


class Command(ABC):
    def __init__(self, name: str, subparsers: _SubParsersAction) -> None:
        parser: ArgumentParser = subparsers.add_parser(
            name=name,
            description=self.HELP,
        )
        parser.add_argument(
            "-v",
            "--verbose",
            dest="verbose",
            action="store_true",
            help="Increase output verbosity",
        )
        self._add_args(parser)

    @property
    @abstractmethod
    def HELP(self) -> str:  # pragma: no cover
        pass

    @staticmethod
    @abstractmethod
    def _add_args(parser: ArgumentParser) -> None:  # pragma: no cover
        pass

    @staticmethod
    def schedule_notification(item_id: int, due: datetime) -> None:
        command: str = f"send-notification `td show {item_id}`"
        ScheduleService().schedule(command=command, when=due)

    @staticmethod
    def unschedule_notification(item_id: int) -> None:
        command: str = f"send-notification `td show {item_id}`"
        ScheduleService().unschedule(command=command)

    @staticmethod
    @abstractmethod
    def run(args: Namespace) -> None:  # pragma: no cover
        pass
