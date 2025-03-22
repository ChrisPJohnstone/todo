from datetime import datetime
from unittest.mock import MagicMock, patch

from test_utils import parametrize, TestSet
from todo.utils import DateUtil

FILEPATH: str = "todo.utils.date"


parse_tests: TestSet = {
    "later": {
        "now": datetime(2025, 1, 1),
        "date_string": "later",
        "expected": datetime(2025, 1, 1, 1),
    },
    "now": {
        "now": datetime(2025, 1, 1),
        "date_string": "now",
        "expected": datetime(2025, 1, 1),
    },
    "today": {
        "now": datetime(2025, 1, 1),
        "date_string": "today",
        "expected": datetime(2025, 1, 1),
    },
    "tomorrow": {
        "now": datetime(2025, 1, 1),
        "date_string": "tomorrow",
        "expected": datetime(2025, 1, 2),
    },
    "1 minute": {
        "now": datetime(2025, 1, 1),
        "date_string": "1 minute",
        "expected": datetime(2025, 1, 1, minute=1),
    },
    "85 minutes": {
        "now": datetime(2025, 1, 1),
        "date_string": "85 minutes",
        "expected": datetime(2025, 1, 1, 1, 25),
    },
    "1 hour": {
        "now": datetime(2025, 1, 1),
        "date_string": "1 hour",
        "expected": datetime(2025, 1, 1, 1),
    },
    "25 hours": {
        "now": datetime(2025, 1, 1),
        "date_string": "25 hours",
        "expected": datetime(2025, 1, 2, 1),
    },
    "1 day": {
        "now": datetime(2025, 1, 1),
        "date_string": "1 day",
        "expected": datetime(2025, 1, 2),
    },
    "367 days": {
        "now": datetime(2025, 1, 1),
        "date_string": "367 days",
        "expected": datetime(2026, 1, 3),
    },
    "1 week": {
        "now": datetime(2025, 1, 1),
        "date_string": "1 week",
        "expected": datetime(2025, 1, 8),
    },
    "3 weeks": {
        "now": datetime(2025, 1, 1),
        "date_string": "3 weeks",
        "expected": datetime(2025, 1, 22),
    },
    "monday": {
        "now": datetime(2025, 1, 1),
        "date_string": "monday",
        "expected": datetime(2025, 1, 6),
    },
    "tuesday": {
        "now": datetime(2025, 1, 1),
        "date_string": "tuesday",
        "expected": datetime(2025, 1, 7),
    },
    "wednesday": {
        "now": datetime(2025, 1, 1),
        "date_string": "wednesday",
        "expected": datetime(2025, 1, 8),
    },
    "thursday": {
        "now": datetime(2025, 1, 1),
        "date_string": "thursday",
        "expected": datetime(2025, 1, 2),
    },
    "friday": {
        "now": datetime(2025, 1, 1),
        "date_string": "friday",
        "expected": datetime(2025, 1, 3),
    },
    "saturday": {
        "now": datetime(2025, 1, 1),
        "date_string": "saturday",
        "expected": datetime(2025, 1, 4),
    },
    "sunday": {
        "now": datetime(2025, 1, 1),
        "date_string": "sunday",
        "expected": datetime(2025, 1, 5),
    },
    "2000-02-03 11:22:33": {
        "now": datetime(2025, 1, 1),
        "date_string": "2000-02-03 11:22:33",
        "expected": datetime(2000, 2, 3, 11, 22, 33),
    },
    "2000-02-03 11:22": {
        "now": datetime(2025, 1, 1),
        "date_string": "2000-02-03 11:22",
        "expected": datetime(2000, 2, 3, 11, 22),
    },
    "2000-02-03 11": {
        "now": datetime(2025, 1, 1),
        "date_string": "2000-02-03 11",
        "expected": datetime(2000, 2, 3, 11),
    },
    "2000-02-03": {
        "now": datetime(2025, 1, 1),
        "date_string": "2000-02-03",
        "expected": datetime(2000, 2, 3),
    },
    "05/06/2001 11:22:33": {
        "now": datetime(2025, 1, 1),
        "date_string": "05/06/2001 11:22:33",
        "expected": datetime(2001, 6, 5, 11, 22, 33),
    },
    "05/06/2001 11:22": {
        "now": datetime(2025, 1, 1),
        "date_string": "05/06/2001 11:22",
        "expected": datetime(2001, 6, 5, 11, 22),
    },
    "05/06/2001 11": {
        "now": datetime(2025, 1, 1),
        "date_string": "05/06/2001 11",
        "expected": datetime(2001, 6, 5, 11),
    },
    "05/06/2001": {
        "now": datetime(2025, 1, 1),
        "date_string": "05/06/2001",
        "expected": datetime(2001, 6, 5),
    },
    "never": {
        "now": datetime(2025, 1, 1),
        "date_string": "never",
        "expected": None,
    },
    "none": {
        "now": datetime(2025, 1, 1),
        "date_string": "none",
        "expected": None,
    },
    "na": {"now": datetime(2025, 1, 1), "date_string": "na", "expected": None},
    "n/a": {
        "now": datetime(2025, 1, 1),
        "date_string": "n/a",
        "expected": None,
    },
}


@patch(f"{FILEPATH}.datetime")
@parametrize(parse_tests)
def test_parse(
    mock_datetime: MagicMock,
    now: datetime,
    date_string: str,
    expected: datetime | None,
) -> datetime | None:
    mock_datetime.now.return_value = now
    mock_datetime.strptime.side_effect = datetime.strptime
    assert DateUtil.parse(date_string) == expected


format_tests: TestSet = {
    "2000-02-03 11:22:33": {
        "date": datetime(2000, 2, 3, 11, 22, 33),
        "expected": "2000-02-03 11:22:33",
    },
    "2025-12-31 23:59:59": {
        "date": datetime(2025, 12, 31, 23, 59, 59),
        "expected": "2025-12-31 23:59:59",
    },
    "None": {"date": None, "expected": None},
    "Incomplete": {
        "date": datetime(2025, 1, 1),
        "expected": "2025-01-01 00:00:00",
    },
}


@parametrize(format_tests)
def test_format(date: datetime | None, expected: str) -> None:
    assert DateUtil.format(date) == expected
