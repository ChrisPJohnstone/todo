from argparse import ArgumentParser, Namespace

from ._base import Command
from todo.parsers import query
from todo.services import DatabaseService
from todo.utils import TableFormatter


class Query(Command):
    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return [query()]

    def __init__(self, args: Namespace) -> None:
        query: str = " ".join(args.query)
        database: DatabaseService = DatabaseService()
        results: list[tuple] = database.execute(query)
        if len(results) >= 0:
            print(TableFormatter(results[1:], headers=results[0]))
