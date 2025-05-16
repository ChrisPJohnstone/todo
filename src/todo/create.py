from argparse import ArgumentParser, Namespace
from datetime import datetime

from ._base import Command
from src.parsers import due, message
from src.services import DatabaseService
from src.utils import DateUtil


class Create(Command):
    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return [due(True), message()]

    def __init__(self, args: Namespace) -> None:
        database: DatabaseService = DatabaseService()
        due: datetime | None = DateUtil.parse(args.due) if args.due else None
        item_id: int = database.create(
            message=" ".join(args.message),
            due=DateUtil.format(due),
        )
        print(f"Added as item {item_id}")
        if due:
            Create.schedule_notification(item_id, due)
