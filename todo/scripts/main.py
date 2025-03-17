#!/usr/bin/env python3
from argparse import _SubParsersAction, ArgumentParser, Namespace
import logging

from todo.commands import Command, Complete, Count, Create, List, Update

COMMANDS: dict[str, type[Command]] = {
    "add": Create,
    "complete": Complete,
    "count": Count,
    "list": List,
    "update": Update,
}


def setup_logging(verbose: bool) -> None:
    level: int = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level)


def main() -> None:
    parser: ArgumentParser = ArgumentParser(
        prog="Todo List Manager",
        description="A simple todo list manager",
    )
    subparsers: _SubParsersAction = parser.add_subparsers(
        dest="command",
        required=True,
    )
    for name, command in COMMANDS.items():
        command(name, subparsers)
    args: Namespace = parser.parse_args()
    setup_logging(args.verbose)
    COMMANDS[args.command].run(args)


if __name__ == "__main__":
    main()
