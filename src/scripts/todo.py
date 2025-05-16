#!/usr/bin/env python3
from argparse import _SubParsersAction, ArgumentParser, Namespace
from sys import argv

from src.commands import COMMAND_DICT
from src.utils import setup_logging


def parse_args(args: list[str]) -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="Todo List Manager",
        description="A simple todo list manager",
    )
    subparsers: _SubParsersAction = parser.add_subparsers(
        dest="command",
        required=True,
    )
    for name, command in COMMAND_DICT.items():
        command(name, subparsers)
    return parser.parse_args(args)


def todo() -> None:
    args: Namespace = parse_args(argv[1:])
    setup_logging(args.verbose)
    COMMAND_DICT[args.command].run(args)


if __name__ == "__main__":  # pragma: no cover
    todo()
