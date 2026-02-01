from argparse import ArgumentParser


def criteria() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(add_help=False)
    parser.add_argument(
        dest="criteria",
        type=str,
        nargs="*",
        help="SQL WHERE statement to filter items",
    )
    return parser
