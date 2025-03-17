from argparse import ArgumentParser, BooleanOptionalAction, Namespace

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
            action=BooleanOptionalAction,
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
        count: int = client.get_count(criteria)
        print(count)
