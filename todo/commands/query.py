from argparse import ArgumentParser, Namespace

from tabulate import tabulate

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
        query: str = " ".join(args.query)
        client: Client = Client()
        results: list[tuple] = client.execute(query, include_headers=True)
        print(tabulate(results[1:], headers=results[0]))
