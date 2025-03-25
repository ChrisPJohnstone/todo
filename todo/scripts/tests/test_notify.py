from logging import DEBUG, INFO
from unittest.mock import _Call, call, patch, MagicMock

from todo.scripts.notify import notify
from test_utils import parametrize, TestSet

FILEPATH: str = "todo.scripts.notify"


notify_tests: TestSet = {
    "minimal": {
        "arg_input": ["feed", "dog"],
        "expected_log_level": INFO,
        "expected_notification_calls": [
            call(title="", application_name=""),
            call().send("feed dog"),
        ],
    },
    "all_args": {
        "arg_input": [
            "--title",
            "reminder",
            "--application-name",
            "chores",
            "empty",
            "washing",
            "machine",
            "-v",
        ],
        "expected_log_level": DEBUG,
        "expected_notification_calls": [
            call(title="reminder", application_name="chores"),
            call().send("empty washing machine"),
        ],
    },
}


@patch(f"{FILEPATH}.NotificationService")
@patch("logging.basicConfig")
@parametrize(notify_tests)
def test_notify(
    mock_log_config: MagicMock,
    mock_notification: MagicMock,
    arg_input: list[str],
    expected_log_level: int,
    expected_notification_calls: list[_Call],
) -> None:
    notify(arg_input)
    mock_log_config.assert_called_once_with(level=expected_log_level)
    mock_notification.assert_has_calls(expected_notification_calls)
