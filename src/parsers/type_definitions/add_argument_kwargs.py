from collections.abc import Callable
from typing import Any, TypedDict


class AddArgumentKwargs(TypedDict, total=False):
    """Type definition for `parser.add_argument` kwargs"""

    nargs: str | int
    default: Any
    type: Callable[[str], Any]
    choices: list[Any]
    required: bool
    help: str
    metavar: str
    dest: str
    deprecated: bool
