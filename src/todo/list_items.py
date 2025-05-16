from argparse import ArgumentParser, Namespace

from tabulate import tabulate

from ._base import Command
from src.parsers import criteria, include_completed
from src.services import DatabaseService
from src.utils import QueryUtil


class ListItems(Command):
    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return [criteria(), include_completed()]

    def __init__(self, args: Namespace) -> None:
        database: DatabaseService = DatabaseService()
        criteria: str = QueryUtil.parse_criteria(
            criteria=args.criteria,
            include_completed=args.include_completed,
        )
        results: list[tuple] = database.get_list(criteria)
        if len(results) <= 1:
            print("No items found")
            return
        print(tabulate(results[1:], headers=results[0]))
