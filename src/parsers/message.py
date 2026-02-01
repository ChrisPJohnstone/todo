from argparse import ArgumentParser

from .type_definitions import AddArgumentKwargs


def message(opt: bool = False) -> ArgumentParser:
    kwargs: AddArgumentKwargs = {
        "type": str,
        "nargs": "+",
        "help": "The todo message to add",
    }
    args: list[str] = []
    if opt:
        args.append("--message")
        kwargs["metavar"] = "message"
    else:
        kwargs["dest"] = "message"
    parser: ArgumentParser = ArgumentParser(add_help=False)
    parser.add_argument(*args, **kwargs)
    return parser
