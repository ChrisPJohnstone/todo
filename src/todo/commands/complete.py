from argparse import ArgumentParser, Namespace
from datetime import datetime

from todo.parsers import item_id
from todo.database import DatabaseClient


def command_parsers() -> list[ArgumentParser]:
    return [item_id("The todo item to complete")]


def main(args: Namespace) -> None:
    now: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database: DatabaseClient = DatabaseClient()
    database.update(
        id=args.id[0],
        fields={"completed": True, "completed_at": now},
    )
