from argparse import ArgumentParser, Namespace
from datetime import datetime

from ._base import Command
from todo.parsers import completed, due, item_id, message
from todo.services import DatabaseService
from todo.utils import DateUtil


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
        database: DatabaseService = DatabaseService()
        fields: dict[str, str | bool | None] = {}
        if args.message:
            fields["message"] = " ".join(args.message)
        if args.due:
            due: datetime | None = DateUtil.parse(args.due)
            fields["due"] = DateUtil.format(due)
        if args.completed:
            fields["completed"] = True
            fields["completed_at"] = DateUtil.format(datetime.now())
        if not fields:
            raise ValueError("No fields to update")
        database.update(args.id[0], fields)
