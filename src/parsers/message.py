from argparse import ArgumentParser
from typing import Callable


def message(opt: bool = False) -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(add_help=False)
    base: Callable = lambda *args, **kwargs: parser.add_argument(
        *args,
        **kwargs,
        type=str,
        nargs="+",
        help="The todo message to add",
    )
    if opt:
        base("--message", metavar="message")
    else:
        base(dest="message")
    return parser
