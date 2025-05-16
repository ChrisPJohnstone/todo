from argparse import ArgumentParser


def query() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(add_help=False)
    parser.add_argument(
        dest="query",
        type=str,
        nargs="+",
        help="Query to use",
    )
    return parser
