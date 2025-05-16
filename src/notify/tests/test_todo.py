from argparse import Namespace

from src.scripts.todo import parse_args
from test_utils import parametrize, TestSet

FILEPATH: str = "src.scripts.todo"


parse_args_tests: TestSet = {
    "create": {
        "args": ["add", "test", "item"],
        "expected": Namespace(
            command="add",
            verbose=False,
            message=["test", "item"],
            due="later",
        ),
    },
    "create_with_due": {
        "args": ["add", "test", "item", "--due", "tomorrow", "-v"],
        "expected": Namespace(
            command="add",
            verbose=True,
            message=["test", "item"],
            due="tomorrow",
        ),
    },
    "complete": {
        "args": ["complete", "1357"],
        "expected": Namespace(command="complete", verbose=False, id=["1357"]),
    },
    "count": {
        "args": ["count"],
        "expected": Namespace(
            command="count",
            verbose=False,
            criteria=[],
            include_completed=False,
        ),
    },
    "count_with_criteria": {
        "args": ["count", "due", "<", "DATE('now')"],
        "expected": Namespace(
            command="count",
            verbose=False,
            criteria=["due", "<", "DATE('now')"],
            include_completed=False,
        ),
    },
    "count_with_completed": {
        "args": [
            "count",
            "due",
            "<",
            "DATE('now')",
            "--include-completed",
        ],
        "expected": Namespace(
            command="count",
            verbose=False,
            criteria=["due", "<", "DATE('now')"],
            include_completed=True,
        ),
    },
    "delete": {
        "args": ["rm", "2468"],
        "expected": Namespace(command="rm", verbose=False, id=["2468"]),
    },
    "list": {
        "args": ["ls"],
        "expected": Namespace(
            command="ls",
            verbose=False,
            criteria=[],
            include_completed=False,
        ),
    },
    "list_with_criteria": {
        "args": ["ls", "due", "<", "DATE('now')"],
        "expected": Namespace(
            command="ls",
            verbose=False,
            criteria=["due", "<", "DATE('now')"],
            include_completed=False,
        ),
    },
    "list_with_completed": {
        "args": [
            "ls",
            "due",
            "<",
            "DATE('now')",
            "--include-completed",
        ],
        "expected": Namespace(
            command="ls",
            verbose=False,
            criteria=["due", "<", "DATE('now')"],
            include_completed=True,
        ),
    },
    "query": {
        "args": ["query", "select", "*", "from", "todo"],
        "expected": Namespace(
            command="query",
            verbose=False,
            query=["select", "*", "from", "todo"],
        ),
    },
    "show": {
        "args": ["show", "7531"],
        "expected": Namespace(command="show", verbose=False, id=["7531"]),
    },
    "update": {
        "args": ["update", "8642"],
        "expected": Namespace(
            command="update",
            verbose=False,
            id=["8642"],
            message=None,
            due=None,
            completed=False,
        ),
    },
    "update_with_message": {
        "args": ["update", "8642", "--message", "new", "message"],
        "expected": Namespace(
            command="update",
            verbose=False,
            id=["8642"],
            message=["new", "message"],
            due=None,
            completed=False,
        ),
    },
    "update_with_due": {
        "args": ["update", "8642", "--due", "tomorrow"],
        "expected": Namespace(
            command="update",
            verbose=False,
            id=["8642"],
            message=None,
            due="tomorrow",
            completed=False,
        ),
    },
    "update_with_completed": {
        "args": ["update", "8642", "--completed"],
        "expected": Namespace(
            command="update",
            verbose=False,
            id=["8642"],
            message=None,
            due=None,
            completed=True,
        ),
    },
    "update_mixed": {
        "args": [
            "update",
            "8642",
            "--message",
            "some",
            "kind",
            "of",
            "message",
            "--due",
            "at some point",
            "--completed",
        ],
        "expected": Namespace(
            command="update",
            verbose=False,
            id=["8642"],
            message=["some", "kind", "of", "message"],
            due="at some point",
            completed=True,
        ),
    },
}


@parametrize(parse_args_tests)
def test_parse_args(args: list[str], expected: Namespace) -> None:
    assert parse_args(args) == expected
