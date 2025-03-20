#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
import logging

from todo.services import NotificationService


def setup_logging(verbose: bool) -> None:
    level: int = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level)


def notify() -> None:
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
    args: Namespace = parser.parse_args()
    setup_logging(args.verbose)
    service: NotificationService = NotificationService(
        title=args.title,
        application_name=args.application_name,
    )
    service.send(" ".join(args.message))


if __name__ == "__main__":
    notify()
