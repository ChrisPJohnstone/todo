from abc import ABC, abstractmethod
from argparse import _SubParsersAction, ArgumentParser, Namespace


class Command(ABC):
    def __init__(self, name: str, subparsers: _SubParsersAction) -> None:
        parser: ArgumentParser = subparsers.add_parser(
            name=name,
            description=self.HELP,
        )
        parser.add_argument(
            "-v",
            "--verbose",
            dest="verbose",
            action="store_true",
            help="Increase output verbosity",
        )
        self._add_args(parser)

    @property
    @abstractmethod
    def HELP(self) -> str:  # pragma: no cover
        pass

    @staticmethod
    @abstractmethod
    def _add_args(parser: ArgumentParser) -> None:  # pragma: no cover
        pass

    @staticmethod
    @abstractmethod
    def run(args: Namespace) -> None:  # pragma: no cover
        pass
