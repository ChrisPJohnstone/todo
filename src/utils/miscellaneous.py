from enum import Enum


class Alignment(Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2


def pad_string(
    value: str,
    width: int,
    alignment: Alignment = Alignment.LEFT,
) -> str:
    match alignment:
        case Alignment.LEFT:
            return f"{value:<{width}}"
        case Alignment.RIGHT:
            return f"{value:>{width}}"
        case Alignment.CENTER:
            return f"{value:^{width}}"
    raise ValueError(f"Unknown alignment: {alignment}")
