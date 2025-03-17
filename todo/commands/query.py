from argparse import ArgumentParser, BooleanOptionalAction, Namespace

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
        parser.add_argument(
            "--show-output",
            action=BooleanOptionalAction,
            default=True,
            help="Show the output of the query",
        )

    @staticmethod
    def run(args: Namespace) -> None:
        query: str = " ".join(args.query)
        client: Client = Client()
        results: list[tuple] = client.execute(
            query=query,
            include_headers=args.show_output,
        )
        if args.show_output:
            print(tabulate(results[1:], headers=results[0]))
