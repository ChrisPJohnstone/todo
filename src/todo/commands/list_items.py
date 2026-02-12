from argparse import ArgumentParser, Namespace

from todo.parsers import criteria, include_completed
from todo.database import DatabaseClient
from todo.utils import TableFormatter, QueryUtil


def command_parsers() -> list[ArgumentParser]:
    return [criteria(), include_completed()]


def main(args: Namespace) -> None:
    database: DatabaseClient = DatabaseClient(logger=args.logger)
    criteria: str = QueryUtil.parse_criteria(
        criteria=args.criteria,
        include_completed=args.include_completed,
    )
    results: list[tuple] = database.get_list(criteria)
    if len(results) <= 1:
        print("No items found")
        return
    print(TableFormatter(results[1:], headers=results[0]))  # type: ignore
