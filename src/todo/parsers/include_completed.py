from argparse import ArgumentParser, BooleanOptionalAction


def include_completed() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(add_help=False)
    parser.add_argument(
        "--include-completed",
        action=BooleanOptionalAction,
        default=False,
        help="Include completed items in output (Default: False)",
    )
    return parser
