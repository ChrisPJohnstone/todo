from test_utils import parametrize, TestSet
from src.utils import QueryUtil


parse_criteria_tests: TestSet = {
    "simple": {
        "criteria": ["priority", "=", "1"],
        "include_completed": False,
        "expected": "WHERE not completed AND priority = 1",
    },
    "with_where": {
        "criteria": ["where", "priority", "=", "1"],
        "include_completed": False,
        "expected": "WHERE not completed AND priority = 1",
    },
    "include_completed": {
        "criteria": ["priority", "=", "1"],
        "include_completed": True,
        "expected": "WHERE priority = 1",
    },
    "no_criteria": {
        "criteria": [],
        "include_completed": False,
        "expected": "WHERE not completed",
    },
    "complex": {
        "criteria": ["priority", "=", "1", "AND", "category", "=", "work"],
        "include_completed": False,
        "expected": "WHERE not completed AND priority = 1 AND category = work",
    },
    "complex_with_completed": {
        "criteria": ["priority", "=", "1", "AND", "category", "=", "work"],
        "include_completed": True,
        "expected": "WHERE priority = 1 AND category = work",
    },
}


@parametrize(parse_criteria_tests)
def test_parse_criteria(
    criteria: list[str],
    include_completed: bool,
    expected: str,
) -> None:
    assert QueryUtil.parse_criteria(criteria, include_completed) == expected
