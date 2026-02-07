from curses import window
from curses.textpad import rectangle
from textwrap import wrap


def message_box(
    win: window,
    x_stop: int,
    y_max: int,
    message: str,
    x_strt: int = 0,
    y_strt: int = 0,
    title: str = "",
) -> None:
    len_x: int = x_stop - x_strt
    if len(title) > len_x - 2:
        raise ValueError(f"Title {title} is longer than box")
    lines: list[str] = wrap(message, len_x - 2)
    max_len_y: int = y_max - y_strt - 2
    if len(lines) > max_len_y:
        lines = lines[: max_len_y - 2]
    y_stop: int = y_strt + len(lines) + 1
    rectangle(win, y_strt, x_strt, y_stop, x_stop)
    title_y: int = 1
    for word in title.split(" "):
        win.addstr(y_strt, title_y, word)
        title_y += len(word) + 1
    for index, line in enumerate(lines):
        win.addstr(y_strt + index + 1, 1, line)
