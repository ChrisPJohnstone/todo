from argparse import ArgumentParser, Namespace

from .base import Command
from todo.database import Client
from todo.utils import QueryUtil


class Count(Command):
    @property
    def HELP(self) -> str:
        return "Count todo items"

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
        count: int = client.get_count(QueryUtil.parse_criteria(args))
        print(count)
