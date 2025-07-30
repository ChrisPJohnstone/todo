from typing import Any

from pytest import MarkDecorator, mark

type TestSet = dict[str, dict[str, Any]]


def parametrize(test_cases: TestSet) -> MarkDecorator:
    """
    Replaces the `@pytest.mark.parametrize` decorator to allow for a more
        readable test case definition.

    Args:
        test_cases (dict[str, dict[str, Any]]): A dictionary where each key is a test case name, and each value is a dictionary of parameters for that test case.
        The keys of the inner dictionaries are the parameter names, and the values are the parameter values.

    Returns:
        MarkDecorator: A pytest mark decorator that can be used to parametrize tests.

    Example:
        cases: dict[str, dict[str, Any]] = {
            "positive": {"x": 1, "y": 2, "expected": 3},
            "negative": {"x": -1, "y": -2, "expected": -3},
        }


        @parametrize(cases)
        def test_function(x: int, y: int, expected: int) -> None:
            assert x + y == expected
    """
    argnames: list[str] = sorted(
        {
            argname
            for test_case in test_cases.values()
            for argname in test_case.keys()
        }
    )
    return mark.parametrize(
        argnames=argnames,
        argvalues=[
            [test_case.get(arg) for arg in argnames]
            for test_case in test_cases.values()
        ],
        ids=list(test_cases.keys()),
    )
