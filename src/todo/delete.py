from argparse import ArgumentParser, Namespace

from ._base import Command
from parsers import item_id
from services import DatabaseService


class Delete(Command):
    @staticmethod
    def parent_parsers() -> list[ArgumentParser]:
        return [item_id("The todo item to delete")]

    def __init__(self, args: Namespace) -> None:
        database: DatabaseService = DatabaseService()
        results: list[tuple] = database.delete(args.id[0])
        if len(results) <= 1:
            print("No items deleted")
            return
