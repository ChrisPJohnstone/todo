from argparse import ArgumentParser, Namespace
from datetime import datetime

from todo.parsers import due, message
from todo.services import DatabaseService
from todo.utils import DateUtil


def command_parsers() -> list[ArgumentParser]:
    return [due(True), message()]


def main(args: Namespace) -> None:
    database: DatabaseService = DatabaseService()
    due: datetime | None = DateUtil.parse(args.due) if args.due else None
    database.create(" ".join(args.message), DateUtil.format(due))
