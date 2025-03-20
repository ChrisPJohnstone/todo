from argparse import ArgumentParser, Namespace
from datetime import datetime

from .base import Command
from todo.services import DatabaseService


class Complete(Command):
    @property
    def HELP(self) -> str:
        return "Complete a todo item"

    @staticmethod
    def _add_args(parser: ArgumentParser) -> None:
        parser.add_argument(
            type=str,
            dest="id",
            help="The todo item to complete",
            nargs=1,
        )

    @staticmethod
    def run(args: Namespace) -> None:
        now: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        database: DatabaseService = DatabaseService()
        database.update(
            id=args.id[0],
            fields={"completed": True, "completed_at": now},
        )
