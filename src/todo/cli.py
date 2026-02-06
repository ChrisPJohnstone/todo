from argparse import (
    ArgumentParser,
    Namespace,
    RawTextHelpFormatter,
    _SubParsersAction,
)
from collections.abc import Callable
from logging import DEBUG, basicConfig, getLogger

from todo.commands import COMMANDS
from todo.constants import Commands, HELP_COMMANDS
from todo.daemon import Daemon
from todo.parsers import verbose


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
        command_parser: ArgumentParser = subparsers.add_parser(
            name=name,
            formatter_class=RawTextHelpFormatter,
            parents=[*shared, *command.command_parsers()],
            help=HELP_COMMANDS[Commands(name)],
            description=HELP_COMMANDS[Commands(name)],
        )
        command_parser.set_defaults(main=command.main)
    args: Namespace = parser.parse_args()
    basicConfig()
    args.logger = getLogger(__name__)
    if getattr(args, "verbose", False):
        args.logger.setLevel(level=DEBUG)
    args.main(args)
    Daemon(logger=args.logger).start()
