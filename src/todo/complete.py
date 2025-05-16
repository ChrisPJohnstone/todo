from argparse import ArgumentParser, Namespace
from datetime import datetime

from ._base import Command
from src.parsers import item_id
from src.services import DatabaseService


class Complete(Command):
    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return [item_id("The todo item to complete")]

    def __init__(self, args: Namespace) -> None:
        now: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        database: DatabaseService = DatabaseService()
        database.update(
            id=args.id[0],
            fields={"completed": True, "completed_at": now},
        )
        Complete.unschedule_notification(args.id[0])
