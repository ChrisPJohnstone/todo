from collections.abc import Sequence
from pathlib import Path
from sqlite3 import Connection, Cursor, connect
from typing import Any, Final
import logging


class DatabaseClient:
    DATE_PATTERN: Final[str] = r"%Y-%m-%d %H:%M:%S"

    def __init__(self) -> None:
        self.create_table()

    @property
    def DATABASE(self) -> Path:
        return Path.home() / ".todo.db"

    @property
    def TABLE_NAME(self) -> str:
        return "todo"

    @property
    def ASSET_DIR(self) -> Path:
        return Path(__file__).parent / "assets"

    @property
    def DDL(self) -> str:
        if not hasattr(self, "_DDL"):
            self._DDL: str = self._get_asset("ddl.sql")
        return self._DDL

    @property
    def LIST_QUERY(self) -> str:
        if not hasattr(self, "_LIST_QUERY"):
            self._LIST_QUERY: str = self._get_asset("list.sql")
        return self._LIST_QUERY

    @property
    def COUNT_QUERY(self) -> str:
        if not hasattr(self, "_COUNT_QUERY"):
            self._COUNT_QUERY: str = self._get_asset("count.sql")
        return self._COUNT_QUERY

    @property
    def INSERT_QUERY(self) -> str:
        if not hasattr(self, "_INSERT_QUERY"):
            self._INSERT_QUERY: str = self._get_asset("insert.sql")
        return self._INSERT_QUERY

    @property
    def UPDATE_QUERY(self) -> str:
        if not hasattr(self, "_UPDATE_QUERY"):
            self._UPDATE_QUERY: str = self._get_asset("update.sql")
        return self._UPDATE_QUERY

    @property
    def DELETE_QUERY(self) -> str:
        if not hasattr(self, "_DELETE_QUERY"):
            self._DELETE_QUERY: str = self._get_asset("delete.sql")
        return self._DELETE_QUERY

    def _get_asset(self, filename: str) -> str:
        filepath: Path = self.ASSET_DIR / filename
        if not filepath.exists():
            raise FileNotFoundError(f"{filepath} does not exist")
        if not filepath.is_file():
            raise IsADirectoryError(f"{filepath} is a directory")
        template: str = filepath.read_text()
        return template.format(table_name=self.TABLE_NAME)

    def _execute(
        self,
        connection: Connection,
        query: str,
        params: dict[str, Any] | Sequence[Any] | None = None,
    ) -> list[tuple]:
        cursor: Cursor = connection.cursor()
        cursor.execute(query, params or {})
        output: list[tuple] = cursor.fetchall()
        if cursor.description:
            output.insert(
                0,
                tuple(description[0] for description in cursor.description),
            )
        cursor.close()
        connection.commit()
        return output

    def execute(
        self,
        query: str,
        params: dict[str, Any] | Sequence[Any] | None = None,
    ) -> list[tuple]:
        logging.debug(f"Executing {query} with {params}")
        with connect(self.DATABASE) as connection:
            return self._execute(connection, query, params)

    def create_table(self) -> None:
        self.execute(self.DDL)

    def get_list(self, criteria: str = "") -> list[tuple]:
        query: str = f"{self.LIST_QUERY} {criteria}"
        return self.execute(query)

    def get_count(self, criteria: str = "") -> int:
        return self.execute(f"{self.COUNT_QUERY} {criteria}")[1][0]

    def create(self, message: str, due: str | None = None) -> int:
        params: dict[str, Any] = {"message": message, "due": due}
        return self.execute(self.INSERT_QUERY, params)[1][0]

    def update(self, id: int, fields: dict[str, Any]) -> None:
        if not fields:
            raise ValueError("No fields to update")
        query: str = self.UPDATE_QUERY.format(
            fields=", ".join(f'"{field}" = :{field}' for field in fields),
            id=str(id),
        )
        return self.execute(query, fields)[1][0]

    def delete(self, id: int) -> list[tuple]:
        return self.execute(self.DELETE_QUERY.format(id=id))
