from argparse import ArgumentParser, Namespace

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
        for item in client.get_list(QueryUtil.parse_criteria(args)):
            print(item)
