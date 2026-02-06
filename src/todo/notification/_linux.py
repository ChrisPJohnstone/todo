import subprocess


def _send_notification_linux(
    app_name: str,
    expiry_time: int,
    message: str,
) -> None:
    args: list[str] = [
        "notify-send",
        "--app-name",
        app_name,
        "--expire-time",
        str(expiry_time * 1000),
        message,
    ]
    subprocess.run(args)
    # TODO: Maybe don't rely on `notify-send` existing
