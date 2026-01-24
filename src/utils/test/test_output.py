from unittest.mock import PropertyMock, patch

from constants import Alignment
from test_utils import parametrize, TestSet
from type_definitions import Cell, Row, Rows
from utils import TableFormatter

table_formatter_tests: TestSet = {
    "basic_table": {
        "max_width": 50,
        "rows": [["Alice", "24"], ["Bob", "30"]],
        "headers": ["Name", "Age"],
        "column_seperator": " | ",
        "divide_all_lines": False,
        "header_alignment": Alignment.LEFT,
        "row_alignment": Alignment.LEFT,
        "expected": "Name  | Age\n----- | ---\nAlice | 24 \nBob   | 30 ",
    },
    "wrapped_lines": {
        "max_width": 20,
        "rows": [["Alice in Wonderland", "24"], ["Bob the Builder", "30"]],
        "headers": ["Name", "Age"],
        "column_seperator": " | ",
        "divide_all_lines": False,
        "header_alignment": Alignment.LEFT,
        "row_alignment": Alignment.LEFT,
        "expected": (
            "Name           | Age\n"
            "-------------- | ---\n"
            "Alice in       | 24 \n"
            "Wonderland     |    \n"
            "-------------- | ---\n"
            "Bob the        | 30 \n"
            "Builder        |    "
        ),
    },
}


@patch.object(TableFormatter, "max_width", new_callable=PropertyMock)
@parametrize(table_formatter_tests)
def test_table_formatter(
    mock_max_width: PropertyMock,
    max_width: int,
    rows: Rows,
    headers: Row,
    column_seperator: str,
    divide_all_lines: bool,
    header_alignment: Alignment,
    row_alignment: Alignment,
    expected: str,
) -> None:
    mock_max_width.return_value = max_width
    formatter: TableFormatter = TableFormatter(
        rows=rows,
        headers=headers,
        column_seperator=column_seperator,
        divide_all_lines=divide_all_lines,
        header_alignment=header_alignment,
        row_alignment=row_alignment,
    )
    assert str(formatter) == expected
