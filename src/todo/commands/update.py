from argparse import ArgumentParser, Namespace
from datetime import datetime

from todo.parsers import completed, due, item_id, message
from todo.database import DatabaseClient
from todo.utils import DateUtil


def command_parsers() -> list[ArgumentParser]:
    return [
        item_id("The todo item to show"),
        message(opt=True),
        due(),
        completed(),
    ]


def main(args: Namespace) -> None:
    database: DatabaseClient = DatabaseClient()
    fields: dict[str, str | bool | None] = {}
    print("test")
    quit()
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
