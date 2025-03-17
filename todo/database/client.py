from collections.abc import Sequence
from pathlib import Path
from sqlite3 import Cursor, connect
from typing import Any
import logging


class Client:
    def __init__(self) -> None:
        self.create_table()

    @property
    def DATABASE(self) -> Path:
        return Path(__file__).parent / "todo.db"

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
        return f'SELECT COUNT(*) FROM "{self.TABLE_NAME}"'

    @property
    def INSERT_QUERY(self) -> str:
        return f"""
        INSERT INTO "{self.TABLE_NAME}" ("message", "due")
        VALUES (:message, :due)
        RETURNING "id"
        """

    def _execute(
        self,
        query: str,
        params: dict[str, Any] | Sequence[Any] | None = None,
    ) -> list[tuple]:
        logging.debug(f"Executing {query} with {params}")
        with connect(self.DATABASE) as connection:
            cursor: Cursor = connection.cursor()
            cursor.execute(query, params or {})
            output: list[tuple] = cursor.fetchall()
            cursor.close()
            connection.commit()
        return output

    def create_table(self) -> None:
        self._execute(self.DDL)

    def get_list(self, criteria: str = "") -> list[tuple]:
        return self._execute(f"{self.LIST_QUERY} {criteria}")

    def get_count(self, criteria: str = "") -> int:
        return self._execute(f"{self.COUNT_QUERY} {criteria}")[0][0]

    def add(self, message: str, due: str | None = None) -> int:
        params: dict[str, Any] = {"message": message, "due": due}
        return self._execute(self.INSERT_QUERY, params)[0][0]

    def update(self, id: int, fields: dict[str, Any]) -> None:
        query: str = f"""
        UPDATE "{self.TABLE_NAME}"
        SET {", ".join(f"{key} = :{key}" for key in fields)}
        WHERE "id" = {id}
        """
        self._execute(query, fields)
