from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from datetime import datetime
from os import getenv


class Command(ABC):
    @staticmethod
    @abstractmethod
    def parent_parsers() -> list[ArgumentParser]:
        pass

    @abstractmethod
    def __init__(self, args: Namespace) -> None:
        pass
