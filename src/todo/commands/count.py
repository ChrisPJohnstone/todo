from argparse import ArgumentParser, Namespace

from todo.parsers import criteria, include_completed
from todo.services import DatabaseService
from todo.utils import QueryUtil


def command_parsers() -> list[ArgumentParser]:
    return [criteria(), include_completed()]


def main(args: Namespace) -> None:
    database: DatabaseService = DatabaseService()
    parsed_criteria: str = QueryUtil.parse_criteria(
        criteria=args.criteria,
        include_completed=args.include_completed,
    )
    count: int = database.get_count(parsed_criteria)
    print(count)
