from argparse import ArgumentParser, Namespace
from datetime import datetime

from .base import Command
from src.services import DatabaseService
from src.utils import DateUtil


class Create(Command):
    @property
    def HELP(self) -> str:
        return "Add a new todo item"

    @staticmethod
    def _add_args(parser: ArgumentParser) -> None:
        parser.add_argument(
            type=str,
            dest="message",
            help="The todo item to add",
            nargs="+",
        )
        parser.add_argument(
            "--due",
            metavar="due",
            type=str,
            required=False,
            default="later",
            help="When the item is due",
        )

    @staticmethod
    def run(args: Namespace) -> None:
        database: DatabaseService = DatabaseService()
        due: datetime | None = DateUtil.parse(args.due) if args.due else None
        item_id: int = database.create(
            message=" ".join(args.message),
            due=DateUtil.format(due),
        )
        print(f"Added as item {item_id}")
        if due:
            Create.schedule_notification(item_id, due)
