from logging import DEBUG, INFO
from unittest.mock import _Call, call, patch, MagicMock

from test_utils import parametrize, TestSet
from todo.utils import setup_logging

FILEPATH: str = "todo.utils.logger"


setup_logging_tests: TestSet = {
    "info": {
        "verbose": False,
        "expected_calls": [call.basicConfig(level=INFO)],
    },
    "debug": {
        "verbose": True,
        "expected_calls": [call.basicConfig(level=DEBUG)],
    },
}


@patch(f"{FILEPATH}.logging")
@parametrize(setup_logging_tests)
def test_setup_logging(
    mock_logging: MagicMock,
    verbose: bool,
    expected_calls: list[_Call],
) -> None:
    mock_logging.INFO = INFO
    mock_logging.DEBUG = DEBUG
    setup_logging(verbose)
    mock_logging.assert_has_calls(expected_calls)
