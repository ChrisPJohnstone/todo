from argparse import ArgumentParser, Namespace
from datetime import datetime

from ._base import Command
from parsers import completed, due, item_id, message
from services import DatabaseService, ScheduleService
from utils import DateUtil


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
            scheduler: ScheduleService = ScheduleService()
            if args.message:
                message: str = " ".join(args.message)
            else:
                criteria: str = f'WHERE "id" = {args.id[0]}'
                results: list[tuple] = database.get_list(criteria)
                message: str = results[1][results[0].index("message")]
            scheduler.schedule_notification(due, message)
        if args.completed:
            fields["completed"] = True
            fields["completed_at"] = DateUtil.format(datetime.now())
        if not fields:
            raise ValueError("No fields to update")
        database.update(args.id[0], fields)
