from argparse import ArgumentParser, Namespace

from .base import Command
from todo.database import Client


class Query(Command):
    @property
    def HELP(self) -> str:
        return "Query the database"

    @staticmethod
    def _add_args(parser: ArgumentParser) -> None:
        parser.add_argument(
            type=str,
            dest="query",
            help="Query to send",
            nargs="*",
        )

    @staticmethod
    def run(args: Namespace) -> None:
        client: Client = Client()
        for row in client.query(" ".join(args.query)):
            print(row)
