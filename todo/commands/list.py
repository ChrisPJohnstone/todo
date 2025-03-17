from argparse import ArgumentParser, Namespace

from .base import Command
from todo.database import Client


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

    @staticmethod
    def run(args: Namespace) -> None:
        client: Client = Client()
        # TODO: Make filtering more robust and add shorthands
        for item in client.list(" ".join(args.criteria)):
            print(item)
