from argparse import ArgumentParser, Namespace

from .base import Command
from todo.database import Client


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
        client: Client = Client()
        client.delete(args.id[0])
