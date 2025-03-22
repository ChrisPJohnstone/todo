from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from pytest import mark

from todo.utils import DateUtil

FILEPATH: str = "todo.utils.date"


parse_args: list[str] = ["now_return", "date", "expected"]
parse_tests: list[tuple[datetime, str, datetime | None]] = [
    (datetime(2025, 1, 1), "later", datetime(2025, 1, 1, 1)),
    (datetime(2025, 1, 1), "now", datetime(2025, 1, 1)),
    (datetime(2025, 1, 1), "today", datetime(2025, 1, 1)),
    (datetime(2025, 1, 1), "tomorrow", datetime(2025, 1, 2)),
    (datetime(2025, 1, 1), "1 minute", datetime(2025, 1, 1, minute=1)),
    (datetime(2025, 1, 1), "85 minutes", datetime(2025, 1, 1, 1, 25)),
    (datetime(2025, 1, 1), "1 hour", datetime(2025, 1, 1, 1)),
    (datetime(2025, 1, 1), "25 hours", datetime(2025, 1, 2, 1)),
    (datetime(2025, 1, 1), "1 day", datetime(2025, 1, 2)),
    (datetime(2025, 1, 1), "367 days", datetime(2026, 1, 3)),
    (datetime(2025, 1, 1), "1 week", datetime(2025, 1, 8)),
    (datetime(2025, 1, 1), "3 weeks", datetime(2025, 1, 22)),
    (datetime(2025, 1, 1), "monday", datetime(2025, 1, 6)),
    (datetime(2025, 1, 1), "tuesday", datetime(2025, 1, 7)),
    (datetime(2025, 1, 1), "wednesday", datetime(2025, 1, 8)),
    (datetime(2025, 1, 1), "thursday", datetime(2025, 1, 2)),
    (datetime(2025, 1, 1), "friday", datetime(2025, 1, 3)),
    (datetime(2025, 1, 1), "saturday", datetime(2025, 1, 4)),
    (datetime(2025, 1, 1), "sunday", datetime(2025, 1, 5)),
    (
        datetime(2025, 1, 1),
        "2000-02-03 11:22:33",
        datetime(2000, 2, 3, 11, 22, 33),
    ),
    (datetime(2025, 1, 1), "2000-02-03 11:22", datetime(2000, 2, 3, 11, 22)),
    (datetime(2025, 1, 1), "2000-02-03 11", datetime(2000, 2, 3, 11)),
    (datetime(2025, 1, 1), "2000-02-03", datetime(2000, 2, 3)),
    (
        datetime(2025, 1, 1),
        "05/06/2001 11:22:33",
        datetime(2001, 6, 5, 11, 22, 33),
    ),
    (datetime(2025, 1, 1), "05/06/2001 11:22", datetime(2001, 6, 5, 11, 22)),
    (datetime(2025, 1, 1), "05/06/2001 11", datetime(2001, 6, 5, 11)),
    (datetime(2025, 1, 1), "05/06/2001", datetime(2001, 6, 5)),
    (datetime(2025, 1, 1), "never", None),
    (datetime(2025, 1, 1), "none", None),
    (datetime(2025, 1, 1), "na", None),
    (datetime(2025, 1, 1), "n/a", None),
]


@patch(f"{FILEPATH}.datetime")
@mark.parametrize(parse_args, parse_tests)
def test_parse(
    mock_datetime: MagicMock,
    now_return: datetime,
    date: str,
    expected: datetime | None,
) -> datetime | None:
    mock_datetime.now.return_value = now_return
    mock_datetime.strptime.side_effect = datetime.strptime
    assert DateUtil.parse(date) == expected
