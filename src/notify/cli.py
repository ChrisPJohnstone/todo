from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from services import NotificationService


def main() -> None:
    parser: ArgumentParser = ArgumentParser(
        prog="CLI Notification Tool",
        description="A simple CLI tool to send notifications",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "message",
        type=str,
        nargs="+",
        help="The notification message to send",
    )
    args: Namespace = parser.parse_args()
    notification_service: NotificationService = NotificationService()
    notification_service.send_notification(" ".join(args.message))
