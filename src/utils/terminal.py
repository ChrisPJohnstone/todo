from shutil import get_terminal_size


def terminal_width() -> int:
    """Get the width of the terminal."""
    return get_terminal_size().columns
    # TODO: Handle cases where terminal size cannot be determined.
