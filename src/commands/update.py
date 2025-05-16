from argparse import ArgumentParser, Namespace
from datetime import datetime

from .base import Command
from src.services import DatabaseService
from src.utils import DateUtil


class Update(Command):
    @property
    def HELP(self) -> str:
        return "Update a todo item"

    @staticmethod
    def _add_args(parser: ArgumentParser) -> None:
        parser.add_argument(
            type=str,
            dest="id",
            help="The todo item to update",
            nargs=1,
        )
        parser.add_argument(
            "--message",
            metavar="message",
            type=str,
            nargs="+",
            required=False,
            help="New message for the todo item",
        )
        parser.add_argument(
            "--due",
            metavar="due",
            type=str,
            required=False,
            help="New due date for the todo item",
        )
        parser.add_argument(
            "--completed",
            action="store_true",
            help="Mark the todo item as completed",
        )

    @staticmethod
    def run(args: Namespace) -> None:
        fields: dict[str, str | bool | None] = {}
        if args.message:
            fields["message"] = " ".join(args.message)
        if args.due:
            due: datetime | None = DateUtil.parse(args.due)
            fields["due"] = DateUtil.format(due)
            if due is not None and not args.completed:
                Update.schedule_notification(args.id[0], due)
        if args.completed:
            fields["completed"] = True
            fields["completed_at"] = DateUtil.format(datetime.now())
            Update.unschedule_notification(args.id[0])
        if not fields:
            raise ValueError("No fields to update")
        database: DatabaseService = DatabaseService()
        database.update(args.id[0], fields)
