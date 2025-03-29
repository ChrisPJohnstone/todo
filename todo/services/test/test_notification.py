from unittest.mock import _Call, call, patch, MagicMock

from todo.services import NotificationService
from test_utils import parametrize, TestSet

FILEPATH: str = "todo.services.notification"


send_tests: TestSet = {
    "default": {
        "title": "",
        "application_name": "",
        "message": "once upon a time",
        "expected_calls": [
            call(
                default_notification_title="TODO",
                default_notification_message="once upon a time",
                default_notification_application_name="TODO",
            ),
            call().send(),
        ],
    },
    "explicit": {
        "title": "foo",
        "application_name": "bar",
        "message": "there was a man",
        "expected_calls": [
            call(
                default_notification_title="foo",
                default_notification_message="there was a man",
                default_notification_application_name="bar",
            ),
            call().send(),
        ],
    },
}


@patch(f"{FILEPATH}.Notify")
@parametrize(send_tests)
def test_send(
    mock_notify: MagicMock,
    title: str,
    application_name: str,
    message: str,
    expected_calls: list[_Call],
) -> None:
    service: NotificationService = NotificationService(title, application_name)
    service.send(message)
    mock_notify.assert_has_calls(expected_calls)
