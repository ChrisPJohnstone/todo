import logging


def setup_logging(verbose: bool) -> None:
    level: int = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level)
