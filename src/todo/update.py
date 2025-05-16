from argparse import ArgumentParser, Namespace
from datetime import datetime

from ._base import Command
from src.parsers import completed, due, item_id, message
from src.services import DatabaseService
from src.utils import DateUtil


class Update(Command):
    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return [
            item_id("The todo item to show"),
            message(opt=True),
            due(),
            completed(),
        ]

    def __init__(self, args: Namespace) -> None:
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
