from argparse import ArgumentParser, Namespace

from todo.parsers import item_id
from todo.database import DatabaseClient


def command_parsers() -> list[ArgumentParser]:
    return [item_id("The todo item to delete")]


def main(args: Namespace) -> None:
    database: DatabaseClient = DatabaseClient()
    results: list[tuple] = database.delete(args.id[0])
    if len(results) <= 1:
        print("No items deleted")
        return
