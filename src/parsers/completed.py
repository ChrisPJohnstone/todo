from argparse import ArgumentParser


def completed() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(add_help=False)
    parser.add_argument(
        "--completed",
        default=False,
        action="store_true",
        help="Mark the todo item as completed (Default: False)",
    )
    return parser
