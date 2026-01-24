#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace

from .miscellaneous import Alignment, pad_string
from .terminal import terminal_width
from type_definitions import Cell, Row, Rows


class TableFormatter:
    """A simple table formatter for terminal output."""

    DEFAULT_COLUMN_SEPERATOR: str = " | "
    DEFAULT_DIVIDE_ALL_LINES: bool = False

    def __init__(
        self,
        rows: Rows,
        headers: Row | None = None,
        column_seperator: str | None = None,
        divide_all_lines: bool = DEFAULT_DIVIDE_ALL_LINES,
    ) -> None:
        """
        Print data in a table format to the terminal.

        Args:
            data (Rows): An iterable of rows, where each row is an iterable of cell values.
            headers (Row | None): An optional iterable of header names for the table columns.
            column_seperator (str | None): An optional string to separate columns. Defaults to " | ".
            divide_all_lines (bool): Whether to divide all lines with a separating line. Defaults to False.
        """
        if headers is not None:
            self.headers = headers
        self.rows = rows
        if column_seperator is not None:
            self.column_seperator = column_seperator
        self.divide_all_lines = divide_all_lines

    @property
    def max_width(self) -> int:
        """Width of users terminal instance"""
        if not hasattr(self, "_max_width"):
            self._max_width: int = terminal_width()
        return self._max_width

    @property
    def headers(self) -> Row:
        """Header row of the table"""
        return self._headers

    @headers.setter
    def headers(self, value: Row) -> None:
        self._headers: Row = value

    @property
    def has_headers(self) -> bool:
        """Whether the table has headers"""
        return hasattr(self, "_headers")

    @property
    def rows(self) -> Rows:
        """Rows of the table"""
        return self._rows

    @rows.setter
    def rows(self, value: Rows) -> None:
        self._rows: Rows = value

    @property
    def n_rows(self) -> int:
        """Number of rows in the table"""
        if not hasattr(self, "_n_rows"):
            self._n_rows: int = len(self.rows)
        return self._n_rows

    @property
    def n_columns(self) -> int:
        if not hasattr(self, "_n_columns"):
            if self.has_headers:
                self._n_columns: int = len(self.headers)
            else:
                self._n_columns: int = len(self.rows[0])
        return self._n_columns

    @property
    def column_widths(self) -> list[int]:
        """List of column widths"""
        if not hasattr(self, "_column_widths"):
            column_widths: list[int] = []
            for index in range(self.n_columns):
                column_widths.append(self.column_width(index))
            self.column_widths = column_widths
        return self._column_widths

    @column_widths.setter
    def column_widths(self, value: list[int]) -> None:
        width_seperators: int = len(self.column_seperator) * (len(value) - 1)
        width_total: int = sum(value) + width_seperators
        if width_total <= self.max_width:
            self._column_widths: list[int] = value
            return
        self._column_widths = self.distribute_column_widths(value)
        self.divide_all_lines = True

    @property
    def column_seperator(self) -> str:
        """Column seperator string"""
        if not hasattr(self, "_column_seperator"):
            self._column_seperator: str = self.DEFAULT_COLUMN_SEPERATOR
        return self._column_seperator

    @property
    def dividing_line(self) -> str:
        """String representation of the dividing line"""
        if not hasattr(self, "_dividing_line"):
            self._dividing_line: str = self.generate_dividing_line()
        return self._dividing_line

    @property
    def table_string(self) -> str:
        """String representation of the table"""
        if not hasattr(self, "_table_string"):
            self._table_string: str = self.generate_table_string()
        return self._table_string

    def column_width(self, index: int) -> int:
        """
        Calculate the width of a column based on the maximum width of its cells.

        Args:
            index (int): The index of the column.

        Returns:
            int: The width of the column.
        """
        width: int = 0
        if self.has_headers:
            len_header: int = len(str(self.headers[index]))
            if len_header > width:
                width = len_header
        for row_index in range(self.n_rows):
            cell: Cell = self.rows[row_index][index]
            len_cell: int = len(str(cell))
            if len_cell > width:
                width = len_cell
        return width

    def distribute_column_widths(self, original_widths: list[int]) -> list[int]:
        """
        Distribute column widths to fit within the maximum width.
        If a column's width is less than the average remaining width, it is kept as is.

        Args:
            original_widths (list[int]): The original widths of the columns.

        Returns:
            list[int]: The adjusted widths of the columns.
        """
        seperator_width: int = len(self.column_seperator)
        total_seperator_width: int = seperator_width * (self.n_columns - 1)
        remaining_width: int = self.max_width - total_seperator_width
        unresolved: list[int] = list(range(self.n_columns))
        resolved: dict[int, int] = {}
        while len(unresolved) > 0:
            remaining_avg: int = remaining_width // len(unresolved)
            for index, width in enumerate(original_widths):
                if index in resolved:
                    continue
                if width <= remaining_avg:
                    resolved[index] = width
                    unresolved.remove(index)
                    remaining_width -= width
                    break
                if index == unresolved[-1]:
                    resolved[index] = remaining_avg
                    unresolved.remove(index)
                    remaining_width -= remaining_avg
                    continue
        return [resolved[i] for i in range(self.n_columns)]

    def generate_dividing_line(self) -> str:
        """
        Generate the dividing line string.

        Returns:
            str: The dividing line string.
        """
        cells: list[str] = ["-" * width for width in self.column_widths]
        return self.column_seperator.join(cells)

    def wrap_string(self, value: str, width: int) -> list[str]:
        """
        Wrap a string to fit within a specified width.

        Args:
            value (str): The string to wrap.
            width (int): The maximum width of each line.

        Returns:
            list[str]: A list of wrapped lines.
        """
        if len(value) <= width:
            return [value]
        lines: list[str] = []
        current_line: str = ""
        for word in value.split(" "):
            len_current_line: int = len(current_line)
            if len_current_line + len(word) + 1 <= width:
                if len_current_line > 0:
                    current_line += " "
                current_line += word
            else:
                if len_current_line > 0:
                    lines.append(current_line)
                current_line = word
        if len(current_line) > 0:
            lines.append(current_line)
        return lines

    def generate_row_string(self, row: Row, alignment: Alignment) -> str:
        """
        Generate the string representation of a row.

        Args:
            row (Row): The row to generate the string for.

        Returns:
            str: The string representation of the row.
        """
        max_lines: int = 1
        wrapped_cells: list[list[str]] = []
        for index, cell in enumerate(row):
            cell_max_width: int = self.column_widths[index]
            cell_str: str = str(cell)
            if len(cell_str) < cell_max_width:
                cell_padded: str = pad_string(
                    value=cell_str,
                    width=cell_max_width,
                    alignment=alignment,
                )
                wrapped_cells.append([cell_padded])
                continue
            wrapped_cell: list[str] = self.wrap_string(cell_str, cell_max_width)
            n_lines: int = len(wrapped_cell)
            if n_lines > max_lines:
                max_lines = n_lines
            wrapped_cells.append(wrapped_cell)
        lines: list[str] = []
        for line_index in range(max_lines):
            line_cells: list[str] = []
            for cell_index, wrapped_cell in enumerate(wrapped_cells):
                if line_index < len(wrapped_cell):
                    cell_line: str = wrapped_cell[line_index]
                else:
                    cell_line: str = ""
                cell_width: int = self.column_widths[cell_index]
                cell_padded: str = pad_string(
                    value=cell_line,
                    width=cell_width,
                    alignment=alignment,
                )
                line_cells.append(cell_padded)
            lines.append(self.column_seperator.join(line_cells))
        return "\n".join(lines)

    def generate_table_string(self) -> str:
        """
        Generate the string representation of the table.

        Returns:
            str: The string representation of the table.
        """
        lines: list[str] = []
        if self.has_headers:
            line: str = self.generate_row_string(self.headers, Alignment.CENTER)
            lines.append(line)
            lines.append(self.dividing_line)
        for index, row in enumerate(self.rows):
            if len(row) != self.n_columns:
                raise ValueError(f"Row {index} has incorrect number of columns")
            lines.append(self.generate_row_string(row, Alignment.LEFT))
            if self.divide_all_lines and index < self.n_rows - 1:
                lines.append(self.dividing_line)
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.table_string
