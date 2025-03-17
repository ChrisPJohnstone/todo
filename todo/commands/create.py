from argparse import ArgumentParser, Namespace

from .base import Command
from todo.database import Client
from todo.utils import DateUtil


class Create(Command):
    @property
    def HELP(self) -> str:
        return "Add a new todo item"

    @staticmethod
    def _add_args(parser: ArgumentParser) -> None:
        parser.add_argument(
            type=str,
            dest="message",
            help="The todo item to add",
            nargs="*",
        )
        parser.add_argument(
            "--due",
            metavar="due",
            type=str,
            required=False,
            default=None,
            help="When the item is due",
        )

    @staticmethod
    def run(args: Namespace) -> None:
        client: Client = Client()
        item_id: int = client.add(
            message=" ".join(args.message),
            due=DateUtil.format(DateUtil.parse(args.due)) if args.due else None,
        )
        print(f"Added as item {item_id}")
