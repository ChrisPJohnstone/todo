from argparse import ArgumentParser, Namespace
from datetime import datetime

from todo.parsers import item_id
from todo.services import DatabaseService


def command_parsers() -> list[ArgumentParser]:
    return [item_id("The todo item to complete")]


def main(args: Namespace) -> None:
    now: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database: DatabaseService = DatabaseService()
    database.update(
        id=args.id[0],
        fields={"completed": True, "completed_at": now},
    )
