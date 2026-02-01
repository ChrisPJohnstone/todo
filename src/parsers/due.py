from argparse import ArgumentParser

from .type_definitions import AddArgumentKwargs


def due(default: bool = False) -> ArgumentParser:
    kwargs: AddArgumentKwargs = {
        "metavar": "due",
        "type": str,
        "required": False,
        "help": "When the item is due.",
    }
    if default:
        kwargs["default"] = "later"
        kwargs["help"] += " Default: 1 hour from now"
    parser: ArgumentParser = ArgumentParser(add_help=False)
    parser.add_argument("--due", **kwargs)
    return parser
