from argparse import ArgumentParser, Namespace

from tabulate import tabulate

from .base import Command
from todo.services import DatabaseService


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
            nargs="+",
        )

    @staticmethod
    def run(args: Namespace) -> None:
        query: str = " ".join(args.query)
        database: DatabaseService = DatabaseService()
        results: list[tuple] = database.execute(query)
        if len(results) >= 0:
            print(tabulate(results[1:], headers=results[0]))
