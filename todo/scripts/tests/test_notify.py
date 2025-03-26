from argparse import Namespace

from todo.scripts.notify import parse_args
from test_utils import parametrize, TestSet

FILEPATH: str = "todo.scripts.notify"


parse_args_tests: TestSet = {
    "minimal": {
        "args": ["feed", "dog"],
        "expected": Namespace(
            message=["feed", "dog"],
            title="",
            application_name="",
            verbose=False,
        ),
    },
    "all_args": {
        "args": [
            "--title",
            "reminder",
            "--application-name",
            "chores",
            "empty",
            "washing",
            "machine",
            "-v",
        ],
        "expected": Namespace(
            message=["empty", "washing", "machine"],
            title="reminder",
            application_name="chores",
            verbose=True,
        ),
    },
}


@parametrize(parse_args_tests)
def test_parse_args(args: list[str], expected: Namespace) -> None:
    assert parse_args(args) == expected
