#!/usr/bin/env python3
from argparse import _SubParsersAction, ArgumentParser, Namespace
from sys import argv
import logging

from todo.commands import COMMAND_DICT


def setup_logging(verbose: bool) -> None:
    level: int = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level)


def _run(args: Namespace) -> None:  # pragma: no cover
    COMMAND_DICT[args.command].run(args)
    # TODO: Seperate parsers from commands


def todo(arg_input: list[str]) -> None:
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
    args: Namespace = parser.parse_args(arg_input)
    setup_logging(args.verbose)
    _run(args)


if __name__ == "__main__":  # pragma: no cover
    todo(argv)
