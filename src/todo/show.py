from argparse import ArgumentParser, Namespace

from ._base import Command
from src.parsers import item_id
from src.services import DatabaseService


class Show(Command):
    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return [item_id("The todo item to show")]

    def __init__(self, args: Namespace) -> None:
        database: DatabaseService = DatabaseService()
        criteria: str = f'WHERE "id" = {args.id[0]}'
        results: list[tuple] = database.get_list(criteria)
        print(results[1][results[0].index("message")])
