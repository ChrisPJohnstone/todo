#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace

from .terminal import terminal_width
from type_definitions import Cell, Row, Rows


class TableFormatter:
    """A simple table formatter for terminal output."""

    DEFAULT_COLUMN_SEPERATOR: str = " | "

    def __init__(
        self,
        rows: Rows,
        headers: Row | None = None,
        column_seperator: str | None = None,
    ) -> None:
        """
        Print data in a table format to the terminal.

        Args:
            data (Rows): An iterable of rows, where each row is an iterable of cell values.
            headers (Row | None): An optional iterable of header names for the table columns.
        """
        if headers is not None:
            self.headers = headers
        self.rows = rows
        if column_seperator is not None:
            self.column_seperator = column_seperator

    @property
    def max_width(self) -> int:
        """Width of users terminal instance"""
        if not hasattr(self, "_max_width"):
            self._max_width: int = terminal_width()
        return self._max_width
        # TODO: Handle case where table is wider than terminal

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
            self._column_widths: list[int] = column_widths
        return self._column_widths

    @column_widths.setter
    def column_widths(self, value: list[int]) -> None:
        self._column_widths: list[int] = value

    @property
    def column_seperator(self) -> str:
        """Column seperator string"""
        if not hasattr(self, "_column_seperator"):
            self._column_seperator: str = self.DEFAULT_COLUMN_SEPERATOR
        return self._column_seperator

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

    def generate_row_string(self, row: Row) -> str:
        """
        Generate the string representation of a row.

        Args:
            row (Row): The row to generate the string for.

        Returns:
            str: The string representation of the row.
        """
        cell_strings: list[str] = [
            f"{str(cell):<{self.column_widths[index]}}"
            for index, cell in enumerate(row)
        ]
        return self.column_seperator.join(cell_strings)

    def generate_table_string(self) -> str:
        """
        Generate the string representation of the table.

        Returns:
            str: The string representation of the table.
        """
        lines: list[str] = []
        if self.has_headers:
            lines.append(self.generate_row_string(self.headers))
        for index, row in enumerate(self.rows):
            if len(row) != self.n_columns:
                raise ValueError(f"Row {index} has incorrect number of columns")
            lines.append(self.generate_row_string(row))
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.table_string
