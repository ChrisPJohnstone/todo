from os import system


def _send_notification_mac(title: str, message: str) -> None:
    script: str = f'display notification "{message}" with title "{title}"'
    system(f"osascript -e '{script}'")
