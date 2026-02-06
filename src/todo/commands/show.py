from argparse import ArgumentParser, Namespace

from todo.parsers import item_id
from todo.database import DatabaseClient


def command_parsers() -> list[ArgumentParser]:
    return [item_id("The todo item to show")]


def main(args: Namespace) -> None:
    database: DatabaseClient = DatabaseClient(logger=args.logger)
    criteria: str = f'WHERE "id" = {args.id[0]}'
    results: list[tuple] = database.get_list(criteria)
    print(results[1][results[0].index("message")])
