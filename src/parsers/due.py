from argparse import ArgumentParser
from typing import Callable


def due(default: bool = False) -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(add_help=False)
    base: Callable = lambda **kwargs: parser.add_argument(
        "--due",
        metavar="due",
        type=str,
        required=False,
        **kwargs,
    )
    if default:
        base(
            default="later",
            help="When the item is due (Default: 1 Hour from now)",
        )
    else:
        base(help="When the item is due (Default: 1 Hour from now)")
    return parser
