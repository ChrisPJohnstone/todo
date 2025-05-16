from argparse import ArgumentParser, Namespace

from ._base import Command
from src.parsers import criteria, include_completed
from src.services import DatabaseService
from src.utils import QueryUtil


class Count(Command):
    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return [criteria(), include_completed()]

    def __init__(self, args: Namespace) -> None:
        database: DatabaseService = DatabaseService()
        parsed_criteria: str = QueryUtil.parse_criteria(
            criteria=args.criteria,
            include_completed=args.include_completed,
        )
        count: int = database.get_count(parsed_criteria)
        print(count)
