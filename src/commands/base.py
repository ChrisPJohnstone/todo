from abc import ABC, abstractmethod
from argparse import _SubParsersAction, Namespace


class Command(ABC):
    @staticmethod
    @abstractmethod
    def add_parser(subparsers: _SubParsersAction) -> None:  # pragma: no cover
        pass

    @staticmethod
    @abstractmethod
    def run(args: Namespace) -> None:  # pragma: no cover
        pass
