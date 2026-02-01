from argparse import ArgumentParser


def item_id(help_string: str) -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(add_help=False)
    parser.add_argument(
        dest="id",
        type=int,
        nargs=1,
        help=help_string,
    )
    return parser
