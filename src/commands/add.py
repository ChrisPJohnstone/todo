from argparse import _SubParsersAction, ArgumentParser, Namespace

from .base import Command


class Add(Command):
    COMMAND: str = "add"
    HELP: str = "Add a new todo item"

    @staticmethod
    def add_parser(subparsers: _SubParsersAction) -> None:
        parser: ArgumentParser = subparsers.add_parser(
            name=Add.COMMAND,
            description=Add.HELP,
        )
        parser.add_argument(
            type=str,
            dest="message",
            help="The todo item to add",
            nargs="*",
        )

    @staticmethod
    def run(args: Namespace) -> None:
        print(f"Adding todo item: {args.message}")
