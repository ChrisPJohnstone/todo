from argparse import Namespace
from logging import DEBUG, INFO
from unittest.mock import _Call, call, patch, MagicMock, PropertyMock

from todo.scripts import todo
from test_utils import parametrize, TestSet

FILEPATH: str = "todo.scripts.todo"


todo_tests: TestSet = {
    "create": {
        "arg_input": ["add", "test", "item"],
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(
                Namespace(
                    command="add",
                    verbose=False,
                    message=["test", "item"],
                    due="later",
                ),
            ),
        ],
    },
    "create_with_due": {
        "arg_input": ["add", "test", "item", "--due", "tomorrow", "-v"],
        "expected_log_level": DEBUG,
        "expected_run_calls": [
            call(
                Namespace(
                    command="add",
                    verbose=True,
                    message=["test", "item"],
                    due="tomorrow",
                ),
            ),
        ],
    },
    "complete": {
        "arg_input": ["complete", "1357"],
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(Namespace(command="complete", verbose=False, id=["1357"])),
        ],
    },
    "count": {
        "arg_input": ["count"],
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(
                Namespace(
                    command="count",
                    verbose=False,
                    criteria=[],
                    include_completed=False,
                ),
            ),
        ],
    },
    "count_with_criteria": {
        "arg_input": ["count", "due", "<", "DATE('now')"],
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(
                Namespace(
                    command="count",
                    verbose=False,
                    criteria=["due", "<", "DATE('now')"],
                    include_completed=False,
                ),
            ),
        ],
    },
    "count_with_completed": {
        "arg_input": [
            "count",
            "due",
            "<",
            "DATE('now')",
            "--include-completed",
        ],
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(
                Namespace(
                    command="count",
                    verbose=False,
                    criteria=["due", "<", "DATE('now')"],
                    include_completed=True,
                ),
            ),
        ],
    },
    "delete": {
        "arg_input": ["rm", "2468"],
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(Namespace(command="rm", verbose=False, id=["2468"])),
        ],
    },
    "list": {
        "arg_input": ["ls"],
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(
                Namespace(
                    command="ls",
                    verbose=False,
                    criteria=[],
                    include_completed=False,
                ),
            ),
        ],
    },
    "list_with_criteria": {
        "arg_input": ["ls", "due", "<", "DATE('now')"],
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(
                Namespace(
                    command="ls",
                    verbose=False,
                    criteria=["due", "<", "DATE('now')"],
                    include_completed=False,
                ),
            ),
        ],
    },
    "list_with_completed": {
        "arg_input": [
            "ls",
            "due",
            "<",
            "DATE('now')",
            "--include-completed",
        ],
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(
                Namespace(
                    command="ls",
                    verbose=False,
                    criteria=["due", "<", "DATE('now')"],
                    include_completed=True,
                ),
            ),
        ],
    },
    "query": {
        "arg_input": ["query", "select", "*", "from", "todo"],
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(
                Namespace(
                    command="query",
                    verbose=False,
                    query=["select", "*", "from", "todo"],
                ),
            ),
        ],
    },
    "show": {
        "arg_input": ["show", "7531"],
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(Namespace(command="show", verbose=False, id=["7531"])),
        ],
    },
    "update": {
        "arg_input": ["update", "8642"],
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(
                Namespace(
                    command="update",
                    verbose=False,
                    id=["8642"],
                    message=None,
                    due=None,
                    completed=False,
                ),
            ),
        ],
    },
    "update_with_message": {
        "arg_input": ["update", "8642", "--message", "new", "message"],
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(
                Namespace(
                    command="update",
                    verbose=False,
                    id=["8642"],
                    message=["new", "message"],
                    due=None,
                    completed=False,
                ),
            ),
        ],
    },
    "update_with_due": {
        "arg_input": ["update", "8642", "--due", "tomorrow"],
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(
                Namespace(
                    command="update",
                    verbose=False,
                    id=["8642"],
                    message=None,
                    due="tomorrow",
                    completed=False,
                ),
            ),
        ],
    },
    "update_with_completed": {
        "arg_input": ["update", "8642", "--completed"],
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(
                Namespace(
                    command="update",
                    verbose=False,
                    id=["8642"],
                    message=None,
                    due=None,
                    completed=True,
                ),
            ),
        ],
    },
    "update_mixed": {
        "arg_input": [
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
        "expected_log_level": INFO,
        "expected_run_calls": [
            call(
                Namespace(
                    command="update",
                    verbose=False,
                    id=["8642"],
                    message=["some", "kind", "of", "message"],
                    due="at some point",
                    completed=True,
                ),
            ),
        ],
    },
}


@patch(f"{FILEPATH}._run")
@patch("logging.basicConfig")
@parametrize(todo_tests)
def test_notify(
    mock_log_config: MagicMock,
    mock_run: PropertyMock,
    arg_input: list[str],
    expected_log_level: int,
    expected_run_calls: list[_Call],
) -> None:
    todo(arg_input)
    mock_log_config.assert_called_once_with(level=expected_log_level)
    mock_run.assert_has_calls(expected_run_calls)
