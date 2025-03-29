from datetime import datetime
from unittest.mock import _Call, ANY, call, patch, MagicMock

from todo.services import ScheduleService
from test_utils import parametrize, TestSet

FILEPATH: str = "todo.services.schedule"


get_user_tests: TestSet = {
    "testy": {
        "uid": 1,
        "pwuid": ["testy mctestface"],
        "expected": "testy mctestface",
        "expected_getpwuid_calls": [call(1)],
    },
    "boaty": {
        "uid": 5,
        "pwuid": ["boaty mctestface"],
        "expected": "boaty mctestface",
        "expected_getpwuid_calls": [call(5)],
    },
}


@patch(f"{FILEPATH}.getpwuid")
@patch(f"{FILEPATH}.getuid")
@parametrize(get_user_tests)
def test_get_user(
    mock_getuid: MagicMock,
    mock_getpwuid: MagicMock,
    uid: int,
    pwuid: list[str],
    expected: str,
    expected_getpwuid_calls: list[_Call],
) -> None:
    mock_getuid.return_value = uid
    mock_getpwuid.return_value = pwuid
    assert ScheduleService.get_user() == expected
    mock_getpwuid.assert_has_calls(expected_getpwuid_calls)


cron_expression_tests: TestSet = {
    "short": {
        "when": datetime(2025, 1, 2),
        "expected": "0 0 2 1 *",
    },
    "long": {
        "when": datetime(2025, 3, 4, 5, 6, 7, 8),
        "expected": "6 5 4 3 *",
    },
}


@parametrize(cron_expression_tests)
def test_cron_expression(when: datetime, expected: str) -> None:
    assert ScheduleService.cron_expression(when) == expected


schedule_tests: TestSet = {
    "default": {
        "default_user": "testy mctestface",
        "cron_expression": "1 2 3 4 *",
        "user": "",
        "command": "send-notification this is a test",
        "when": datetime(2024, 4, 3, 2, 1),
        "expected_unschedule_calls": [call("send-notification this is a test")],
        "expected_logging_calls": [
            call.debug(
                "Scheduling send-notification this is a test for 2024-04-03 "
                "02:01:00 for testy mctestface"
            )
        ],
        "expected_crontab_calls": [
            call(user="testy mctestface"),
            call().__enter__(),
            call().__enter__().new(command="send-notification this is a test"),
            call().__enter__().new().setall("1 2 3 4 *"),
            call().__exit__(None, None, None),
        ],
        "expected_cron_expression_calls": [call(datetime(2024, 4, 3, 2, 1))],
    },
    "explicit": {
        "default_user": "testy mctestface",
        "cron_expression": "1 2 3 4 *",
        "user": "boaty mctestface",
        "command": "send-notification I'm behind you",
        "when": datetime(2024, 4, 3, 2, 1),
        "expected_unschedule_calls": [call("send-notification I'm behind you")],
        "expected_logging_calls": [
            call.debug(
                "Scheduling send-notification I'm behind you for 2024-04-03 "
                "02:01:00 for boaty mctestface"
            )
        ],
        "expected_crontab_calls": [
            call(user="boaty mctestface"),
            call().__enter__(),
            call().__enter__().new(command="send-notification I'm behind you"),
            call().__enter__().new().setall("1 2 3 4 *"),
            call().__exit__(None, None, None),
        ],
        "expected_cron_expression_calls": [call(datetime(2024, 4, 3, 2, 1))],
    },
}


@patch.object(ScheduleService, "cron_expression")
@patch(f"{FILEPATH}.CronTab")
@patch(f"{FILEPATH}.logging")
@patch.object(ScheduleService, "unschedule")
@patch.object(ScheduleService, "get_user")
@parametrize(schedule_tests)
def test_schedule(
    mock_get_user: MagicMock,
    mock_unschedule: MagicMock,
    mock_logging: MagicMock,
    mock_crontab: MagicMock,
    mock_cron_expression: MagicMock,
    default_user: str,
    cron_expression: str,
    user: str,
    command: str,
    when: datetime,
    expected_unschedule_calls: list[_Call],
    expected_logging_calls: list[_Call],
    expected_crontab_calls: list[_Call],
    expected_cron_expression_calls: list[_Call],
) -> None:
    mock_get_user.return_value = default_user
    mock_cron_expression.return_value = cron_expression
    ScheduleService(user).schedule(command, when)
    mock_unschedule.assert_has_calls(expected_unschedule_calls)
    mock_logging.assert_has_calls(expected_logging_calls)
    mock_crontab.assert_has_calls(expected_crontab_calls)
    mock_cron_expression.assert_has_calls(expected_cron_expression_calls)


unschedule_tests: TestSet = {
    "default": {
        "default_user": "testy mctestface",
        "find_command_return": ["test"],
        "user": "",
        "command": "send-notification you're the one",
        "expected_logging_calls": [
            call.debug(
                "Unscheduling send-notification you're the one for "
                "testy mctestface"
            )
        ],
        "expected_crontab_calls": [
            call(user="testy mctestface"),
            call().__enter__(),
            call().__enter__().find_command("send-notification you're the one"),
            call().__enter__().remove("test"),
            call().__exit__(None, None, None),
        ],
    },
    "explicit": {
        "default_user": "boaty mctestface",
        "find_command_return": ["foo", "bar"],
        "user": "",
        "command": "send-notification the sparrow",
        "expected_logging_calls": [
            call.debug(
                "Unscheduling send-notification the sparrow for "
                "boaty mctestface"
            )
        ],
        "expected_crontab_calls": [
            call(user="boaty mctestface"),
            call().__enter__(),
            call().__enter__().find_command("send-notification the sparrow"),
            call().__enter__().remove("foo"),
            call().__enter__().remove("bar"),
            call().__exit__(None, None, None),
        ],
    },
}


@patch(f"{FILEPATH}.CronTab")
@patch(f"{FILEPATH}.logging")
@patch.object(ScheduleService, "get_user")
@parametrize(unschedule_tests)
def test_unschedule(
    mock_get_user: MagicMock,
    mock_logging: MagicMock,
    mock_crontab: MagicMock,
    default_user: str,
    find_command_return: list[str],
    user: str,
    command: str,
    expected_logging_calls: MagicMock,
    expected_crontab_calls: MagicMock,
) -> None:
    mock_get_user.return_value = default_user
    cron: MagicMock = mock_crontab.return_value.__enter__.return_value
    cron.find_command.return_value = find_command_return
    ScheduleService(user).unschedule(command)
    mock_logging.assert_has_calls(expected_logging_calls)
    mock_crontab.assert_has_calls(expected_crontab_calls)
