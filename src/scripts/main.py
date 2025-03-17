#!/usr/bin/env python3
from argparse import _SubParsersAction, ArgumentParser, Namespace

from src.commands import Add, Command

COMMANDS: dict[str, type[Command]] = {
    Add.COMMAND: Add,
}


def main() -> None:
    parser: ArgumentParser = ArgumentParser(
        prog="Todo List Manager",
        description="A simple todo list manager",
    )
    subparsers: _SubParsersAction = parser.add_subparsers(
        dest="command",
        required=True,
    )
    for command in COMMANDS.values():
        command.add_parser(subparsers)
    args: Namespace = parser.parse_args()
    COMMANDS[args.command].run(args)


if __name__ == "__main__":
    main()
