from argparse import ArgumentParser, Namespace
from typing import Protocol


class CommandModule(Protocol):
    @staticmethod
    def command_parsers() -> list[ArgumentParser]: ...

    @staticmethod
    def main(args: Namespace) -> None: ...
