from argparse import ArgumentParser
from typing import Protocol


class CommandModule(Protocol):
    @staticmethod
    def command_parsers() -> list[ArgumentParser]: ...

    @staticmethod
    def main() -> None: ...
