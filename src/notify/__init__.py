from argparse import ArgumentParser, Namespace
from sys import argv

from src.services import NotificationService
from src.utils import setup_logging


def parse_args(args: list[str]) -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="Notification Program",
        description="Sends a system notification based on input",
    )
    parser.add_argument(
        type=str,
        dest="message",
        help="The message to send",
        nargs="+",
    )
    parser.add_argument(
        "--title",
        metavar="title",
        type=str,
        required=False,
        default="",
        help="The title of the notification",
    )
    parser.add_argument(
        "--application-name",
        metavar="application_name",
        type=str,
        required=False,
        default="",
        help="The application name of the notification",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Increase output verbosity",
    )
    return parser.parse_args(args)


def main() -> None:
    args: Namespace = parse_args(argv[1:])
    setup_logging(args.verbose)
    service: NotificationService = NotificationService(
        title=args.title,
        application_name=args.application_name,
    )
    service.send(" ".join(args.message))
