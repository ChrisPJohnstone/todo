from argparse import (
    ArgumentParser,
    Namespace,
    RawTextHelpFormatter,
    _SubParsersAction,
)
from collections.abc import Callable
import logging

from todo import (
    Command,
    Complete,
    Count,
    Create,
    Delete,
    ListItems,
    Query,
    Show,
    Update,
)
from todo.constants import Commands, HELP_COMMANDS
from todo.parsers import verbose
from todo.services import DaemonService


COMMANDS: dict[str, type[Command]] = {
    Commands.COMPLETE: Complete,
    Commands.COUNT: Count,
    Commands.CREATE: Create,
    Commands.DELETE: Delete,
    Commands.LIST: ListItems,
    Commands.QUERY: Query,
    Commands.SHOW: Show,
    Commands.UPDATE: Update,
}
SHARED_PARSERS: list[Callable[[], ArgumentParser]] = [verbose]


def main() -> None:
    shared: list[ArgumentParser] = [parser() for parser in SHARED_PARSERS]
    parser: ArgumentParser = ArgumentParser(
        prog="Todo List Manager",
        description="A simple todo list manager",
        formatter_class=RawTextHelpFormatter,
        parents=shared,
    )
    subparsers: _SubParsersAction = parser.add_subparsers(
        title="command",
        dest="command",
        metavar="<command>",
        required=True,
    )
    for name, command in COMMANDS.items():
        subparsers.add_parser(
            name=name,
            formatter_class=RawTextHelpFormatter,
            parents=[*shared, *command.parent_parsers()],
            help=HELP_COMMANDS[Commands(name)],
            description=HELP_COMMANDS[Commands(name)],
        )
    args: Namespace = parser.parse_args()
    if getattr(args, "verbose", False):
        logging.basicConfig(level=logging.DEBUG)
    COMMANDS[args.command](args)
    DaemonService().start()
