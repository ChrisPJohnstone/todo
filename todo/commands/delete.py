from argparse import ArgumentParser, Namespace

from .base import Command
from todo.services import DatabaseService


class Delete(Command):
    @property
    def HELP(self) -> str:
        return "Delete a todo item"

    @staticmethod
    def _add_args(parser: ArgumentParser) -> None:
        parser.add_argument(
            type=str,
            dest="id",
            help="The todo item to delete",
            nargs=1,
        )

    @staticmethod
    def run(args: Namespace) -> None:
        database: DatabaseService = DatabaseService()
        results: list[tuple] = database.delete(args.id[0])
        if len(results) <= 1:
            print("No items deleted")
            return
