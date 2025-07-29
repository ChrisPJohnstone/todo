from argparse import ArgumentParser, Namespace

from tabulate import tabulate

from ._base import Command
from parsers import query
from services import DatabaseService


class Query(Command):
    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return [query()]

    def __init__(self, args: Namespace) -> None:
        query: str = " ".join(args.query)
        database: DatabaseService = DatabaseService()
        results: list[tuple] = database.execute(query)
        if len(results) >= 0:
            print(tabulate(results[1:], headers=results[0]))
