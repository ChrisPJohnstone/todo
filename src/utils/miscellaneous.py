from platform import system

from constants import Alignment, Platform


def operating_system() -> Platform:
    try:
        return Platform(system().lower())
    except ValueError:
        raise NotImplementedError(f"Unsupported OS: {system()}")


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
