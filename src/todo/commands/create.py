from argparse import ArgumentParser, Namespace
from datetime import datetime

from todo.parsers import due, message
from todo.database import DatabaseClient
from todo.utils import DateUtil


def command_parsers() -> list[ArgumentParser]:
    return [due(True), message()]


def main(args: Namespace) -> None:
    database: DatabaseClient = DatabaseClient(logger=args.logger)
    due: datetime | None = DateUtil.parse(args.due) if args.due else None
    database.create(" ".join(args.message), DateUtil.format(due))
