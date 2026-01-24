import subprocess


def _send_notification_linux(message: str) -> None:
    subprocess.run(["notify-send", message])
