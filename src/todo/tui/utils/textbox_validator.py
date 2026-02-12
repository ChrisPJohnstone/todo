from ..constants import Key


def textbox_validator(key: int) -> int:
    if key in (Key.CTRL_J, Key.CTRL_M, Key.ENTER):
        return 7  # Ctrl-G
    return key
