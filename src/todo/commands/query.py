from argparse import ArgumentParser, Namespace

from todo.parsers import query
from todo.database import DatabaseClient
from todo.utils import TableFormatter


def command_parsers() -> list[ArgumentParser]:
    return [query()]


def main(args: Namespace) -> None:
    query: str = " ".join(args.query)
    database: DatabaseClient = DatabaseClient(logger=args.logger)
    results: list[tuple] = database.execute(query)
    if len(results) >= 0:
        print(TableFormatter(results[1:], headers=results[0]))  # type: ignore
