from collections.abc import Sequence
from pathlib import Path
from sqlite3 import Connection, Cursor, connect
from typing import Any
import logging


class DatabaseService:
    def __init__(self) -> None:
        self.create_table()

    @property
    def DATABASE(self) -> Path:
        return Path.home() / ".todo.db"

    @property
    def TABLE_NAME(self) -> str:
        return "todo"

    @property
    def DDL(self) -> str:
        return f"""
        CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
            "id"            INTEGER     PRIMARY KEY AUTOINCREMENT,
            "created_at"    TIMESTAMP   NOT NULL    DEFAULT CURRENT_TIMESTAMP,
            "message"       TEXT        NOT NULL,
            "due"           TIMESTAMP   NULL,
            "completed"     BOOLEAN     NOT NULL    DEFAULT 0,
            "completed_at"  TIMESTAMP   NULL
        )
        """

    @property
    def LIST_QUERY(self) -> str:
        return f'SELECT * FROM "{self.TABLE_NAME}"'

    @property
    def COUNT_QUERY(self) -> str:
        return f'SELECT COUNT(*) AS "count" FROM "{self.TABLE_NAME}"'

    @property
    def INSERT_QUERY(self) -> str:
        return f"""
        INSERT INTO "{self.TABLE_NAME}" ("message", "due")
        VALUES (:message, :due)
        RETURNING "id"
        """

    @property
    def UPDATE_QUERY(self) -> str:
        return f"""
        UPDATE "{self.TABLE_NAME}"
        SET {{fields}}
        WHERE "id" = {{id}}
        RETURNING "id"
        """

    @property
    def DELETE_QUERY(self) -> str:
        return f"""
        DELETE FROM "{self.TABLE_NAME}"
        WHERE "id" = {{id}}
        RETURNING "id"
        """

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
            id=id,
        )
        return self.execute(query, fields)[1][0]

    def delete(self, id: int) -> list[tuple]:
        return self.execute(self.DELETE_QUERY.format(id=id))
