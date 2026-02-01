from argparse import ArgumentParser, Namespace

from ._base import Command
from todo.parsers import criteria, include_completed
from todo.services import DatabaseService
from todo.utils import TableFormatter, QueryUtil


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
        print(TableFormatter(results[1:], headers=results[0]))
