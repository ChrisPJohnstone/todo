from argparse import ArgumentParser, Namespace

from todo.parsers import item_id
from todo.services import DatabaseService


def command_parsers() -> list[ArgumentParser]:
    return [item_id("The todo item to show")]


def main(args: Namespace) -> None:
    database: DatabaseService = DatabaseService()
    criteria: str = f'WHERE "id" = {args.id[0]}'
    results: list[tuple] = database.get_list(criteria)
    print(results[1][results[0].index("message")])
