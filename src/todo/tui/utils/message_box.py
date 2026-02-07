from curses import A_ALTCHARSET, A_NORMAL, window
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
    title_attr: int = A_NORMAL,
    message_attr: int = A_NORMAL,
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
        len_word: int = len(word)
        win.addstr(y_strt, title_y, word, title_attr)
        win.chgat(y_strt, title_y + len_word, 1, title_attr | A_ALTCHARSET)
        title_y += len_word + 1
    win.chgat(y_strt, title_y - 1, 1, A_ALTCHARSET)
    for index, line in enumerate(lines):
        win.addstr(y_strt + index + 1, 1, line, message_attr)
