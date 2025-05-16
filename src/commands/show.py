from argparse import ArgumentParser, Namespace

from .base import Command
from src.services import DatabaseService


class Show(Command):
    @property
    def HELP(self) -> str:
        return "Show a todo item"

    @staticmethod
    def _add_args(parser: ArgumentParser) -> None:
        parser.add_argument(
            type=str,
            dest="id",
            help="The todo item to show",
            nargs=1,
        )

    @staticmethod
    def run(args: Namespace) -> None:
        database: DatabaseService = DatabaseService()
        criteria: str = f'WHERE "id" = {args.id[0]}'
        results: list[tuple] = database.get_list(criteria)
        print(results[1][results[0].index("message")])
