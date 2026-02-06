from argparse import ArgumentParser, Namespace

from todo.database import DatabaseClient
from todo.tui import TUI


def command_parsers() -> list[ArgumentParser]:
    return []


def main(args: Namespace) -> None:
    database: DatabaseClient = DatabaseClient()
    TUI(database, args.logger)
