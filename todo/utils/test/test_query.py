from test_utils import parametrize, TestSet
from todo.utils import QueryUtil


parse_criteria_tests: TestSet = {
    "overdue": {
        "criteria": ["where", "due", "<", "CURRENT_TSTAMP"],
        "include_completed": False,
        "expected": "WHERE not completed AND due < CURRENT_TSTAMP",
    },
    "overdue with completed": {
        "criteria": ["due", "<", "CURRENT_TSTAMP"],
        "include_completed": True,
        "expected": "WHERE due < CURRENT_TSTAMP",
    },
    "all": {
        "criteria": [],
        "include_completed": True,
        "expected": "",
    },
    "completed": {
        "criteria": ["completed"],
        "include_completed": True,
        "expected": "WHERE completed",
    },
}


@parametrize(parse_criteria_tests)
def test_parse_criteria(
    criteria: list[str],
    include_completed: bool,
    expected: str,
) -> None:
    assert QueryUtil.parse_criteria(criteria, include_completed) == expected
