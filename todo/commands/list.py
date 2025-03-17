from argparse import ArgumentParser, Namespace

from tabulate import tabulate

from .base import Command
from todo.database import Client
from todo.utils import QueryUtil


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
            action="store_true",
            default=False,
            help="Include completed items in the list",
        )

    @staticmethod
    def run(args: Namespace) -> None:
        client: Client = Client()
        criteria: str = QueryUtil.parse_criteria(
            criteria=args.criteria,
            include_completed=args.include_completed,
        )
        results: list[tuple] = client.get_list(criteria)
        print(tabulate(results[1:], headers=results[0]))
