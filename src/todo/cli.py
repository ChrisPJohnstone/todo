from argparse import (
    ArgumentParser,
    Namespace,
    RawTextHelpFormatter,
    _SubParsersAction,
)
from collections.abc import Callable
import logging

from ._base import Command
from .complete import Complete
from .count import Count
from .create import Create
from .delete import Delete
from .list_items import ListItems
from .query import Query
from .show import Show
from .update import Update
from parsers import verbose


COMMANDS: dict[str, type[Command]] = {
    "add": Create,
    "complete": Complete,
    "count": Count,
    "rm": Delete,
    "ls": ListItems,
    "query": Query,
    "show": Show,
    "update": Update,
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
        help=f"One of:\n- {'\n- '.join(COMMANDS.keys())}",
        required=True,
    )
    for name, command in COMMANDS.items():
        subparsers.add_parser(
            name=name,
            formatter_class=RawTextHelpFormatter,
            parents=[*shared, *command.parent_parsers()],
        )
    args: Namespace = parser.parse_args()
    if getattr(args, "verbose", False):
        logging.basicConfig(level=logging.DEBUG)
    COMMANDS[args.command](args)
