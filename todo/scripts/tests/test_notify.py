from argparse import Namespace
from unittest.mock import _Call, call, patch, MagicMock

from todo.scripts.notify import notify, parse_args
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


notify_tests: TestSet = {
    "default": {
        "args": Namespace(
            title="",
            application_name="",
            verbose=False,
            message=["this", "is", "a", "test"],
        ),
        "expected_setup_logging_calls": [call(False)],
        "expected_service_calls": [
            call(title="", application_name=""),
            call().send("this is a test"),
        ],
    },
    "explicit": {
        "args": Namespace(
            title="foo",
            application_name="bar",
            verbose=True,
            message=["mary's", "little", "lamb"],
        ),
        "expected_setup_logging_calls": [call(True)],
        "expected_service_calls": [
            call(title="foo", application_name="bar"),
            call().send("mary's little lamb"),
        ],
    },
}


@patch(f"{FILEPATH}.NotificationService")
@patch(f"{FILEPATH}.setup_logging")
@patch(f"{FILEPATH}.parse_args")
@parametrize(notify_tests)
def test_notify(
    mock_parse_args: MagicMock,
    mock_setup_logging: MagicMock,
    mock_service: MagicMock,
    args: Namespace,
    expected_setup_logging_calls: list[_Call],
    expected_service_calls: list[_Call],
) -> None:
    mock_parse_args.return_value = args
    notify()
    mock_setup_logging.assert_has_calls(expected_setup_logging_calls)
    mock_service.assert_has_calls(expected_service_calls)
