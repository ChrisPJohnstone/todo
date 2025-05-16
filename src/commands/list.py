from argparse import ArgumentParser, BooleanOptionalAction, Namespace

from tabulate import tabulate

from .base import Command
from src.services import DatabaseService
from src.utils import QueryUtil


class List(Command):
    @property
    def HELP(self) -> str:
        return "List all todo items"

    @staticmethod
    def _add_args(parser: ArgumentParser) -> None:
        parser.add_argument(
            type=str,
            dest="criteria",
            help="SQL WHERE statement to filter items",
            nargs="*",
        )
        parser.add_argument(
            "--include-completed",
            action=BooleanOptionalAction,
            default=False,
            help="Include completed items in the list",
        )

    @staticmethod
    def run(args: Namespace) -> None:
        database: DatabaseService = DatabaseService()
        criteria: str = QueryUtil.parse_criteria(
            criteria=args.criteria,
            include_completed=args.include_completed,
        )
        results: list[tuple] = database.get_list(criteria)
        if len(results) <= 1:
            print("No items found")
            return
        print(tabulate(results[1:], headers=results[0]))
