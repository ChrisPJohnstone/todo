from argparse import ArgumentParser, Namespace

from todo.parsers import criteria, include_completed
from todo.database import DatabaseClient
from todo.utils import QueryUtil


def command_parsers() -> list[ArgumentParser]:
    return [criteria(), include_completed()]


def main(args: Namespace) -> None:
    database: DatabaseClient = DatabaseClient()
    parsed_criteria: str = QueryUtil.parse_criteria(
        criteria=args.criteria,
        include_completed=args.include_completed,
    )
    count: int = database.get_count(parsed_criteria)
    print(count)
