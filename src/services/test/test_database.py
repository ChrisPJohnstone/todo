from typing import Any
from unittest.mock import _Call, call, patch, MagicMock

from pytest import raises

from services import DatabaseService
from test_utils import parametrize, TestSet

FILEPATH: str = "services.database"


def _mock_execute(mock_connect: MagicMock) -> MagicMock:
    mock_connection: MagicMock = (
        mock_connect.return_value.__enter__.return_value
    )
    mock_cursor: MagicMock = mock_connection.cursor
    return mock_cursor.return_value.execute


@patch(f"{FILEPATH}.connect")
def test_init(mock_connect: MagicMock) -> None:
    mock_execute: MagicMock = _mock_execute(mock_connect)
    service: DatabaseService = DatabaseService()
    mock_execute.assert_called_once_with(service.DDL, {})


get_list_tests: TestSet = {
    "no_criteria": {
        "criteria": "",
        "expected_execute_calls": [call('SELECT * FROM "todo" ', {})],
    },
    "criteria": {
        "criteria": "WHERE not completed",
        "expected_execute_calls": [
            call('SELECT * FROM "todo" WHERE not completed', {})
        ],
    },
}


@patch.object(DatabaseService, "__init__", new=MagicMock(return_value=None))
@patch(f"{FILEPATH}.connect")
@parametrize(get_list_tests)
def test_get_list(
    mock_connect: MagicMock,
    criteria: str,
    expected_execute_calls: list[_Call],
) -> None:
    mock_execute: MagicMock = _mock_execute(mock_connect)
    DatabaseService().get_list(criteria)
    mock_execute.assert_has_calls(expected_execute_calls)


get_count_tests: TestSet = {
    "no_criteria": {
        "criteria": "",
        "expected_execute_calls": [
            call('SELECT COUNT(*) AS "count" FROM "todo" ', {})
        ],
    },
    "criteria": {
        "criteria": "WHERE not completed",
        "expected_execute_calls": [
            call(
                'SELECT COUNT(*) AS "count" '
                'FROM "todo" '
                "WHERE not completed",
                {},
            )
        ],
    },
}


@patch.object(DatabaseService, "__init__", new=MagicMock(return_value=None))
@patch(f"{FILEPATH}.connect")
@parametrize(get_count_tests)
def test_get_count(
    mock_connect: MagicMock,
    criteria: str,
    expected_execute_calls: list[_Call],
) -> None:
    mock_execute: MagicMock = _mock_execute(mock_connect)
    DatabaseService().get_count(criteria)
    mock_execute.assert_has_calls(expected_execute_calls)


create_tests: TestSet = {
    "no_due": {
        "message": "Test message",
        "due": None,
        "expected_execute_calls": [
            call(
                'INSERT INTO "todo" ("message", "due") '
                "VALUES (:message, :due) "
                'RETURNING "id"',
                {"message": "Test message", "due": None},
            )
        ],
    },
    "due": {
        "message": "do the dishes",
        "due": "2021-01-01",
        "expected_execute_calls": [
            call(
                'INSERT INTO "todo" ("message", "due") '
                "VALUES (:message, :due) "
                'RETURNING "id"',
                {"message": "do the dishes", "due": "2021-01-01"},
            )
        ],
    },
}


@patch.object(DatabaseService, "__init__", new=MagicMock(return_value=None))
@patch(f"{FILEPATH}.connect")
@parametrize(create_tests)
def test_create(
    mock_connect: MagicMock,
    message: str,
    due: str | None,
    expected_execute_calls: list[_Call],
) -> None:
    mock_execute: MagicMock = _mock_execute(mock_connect)
    DatabaseService().create(message, due)
    mock_execute.assert_has_calls(expected_execute_calls)


update_tests: TestSet = {
    "message": {
        "id": 1234,
        "fields": {"message": "New message"},
        "expected_execute_calls": [
            call(
                'UPDATE "todo" '
                'SET "message" = :message '
                'WHERE "id" = 1234 '
                'RETURNING "id"',
                {"message": "New message"},
            )
        ],
    },
    "due": {
        "id": 5678,
        "fields": {"due": "2021-01-01"},
        "expected_execute_calls": [
            call(
                'UPDATE "todo" '
                'SET "due" = :due '
                'WHERE "id" = 5678 '
                'RETURNING "id"',
                {"due": "2021-01-01"},
            )
        ],
    },
    "completed": {
        "id": 9012,
        "fields": {"completed": True, "completed_at": "2021-01-01"},
        "expected_execute_calls": [
            call(
                'UPDATE "todo" '
                'SET "completed" = :completed, "completed_at" = :completed_at '
                'WHERE "id" = 9012 '
                'RETURNING "id"',
                {"completed": True, "completed_at": "2021-01-01"},
            )
        ],
    },
}


@patch.object(DatabaseService, "__init__", new=MagicMock(return_value=None))
@patch(f"{FILEPATH}.connect")
@parametrize(update_tests)
def test_update(
    mock_connect: MagicMock,
    id: int,
    fields: dict[str, Any],
    expected_execute_calls: list[_Call],
) -> None:
    mock_execute: MagicMock = _mock_execute(mock_connect)
    DatabaseService().update(id, fields)
    mock_execute.assert_has_calls(expected_execute_calls)


@patch.object(DatabaseService, "__init__", new=MagicMock(return_value=None))
def test_update_no_fields() -> None:
    with raises(ValueError, match="No fields to update"):
        DatabaseService().update(1234, {})


delete_tests: TestSet = {
    "1234": {
        "id": 1234,
        "expected_execute_calls": [
            call('DELETE FROM "todo" WHERE "id" = 1234 RETURNING "id"', {})
        ],
    },
    "5678": {
        "id": 5678,
        "expected_execute_calls": [
            call('DELETE FROM "todo" WHERE "id" = 5678 RETURNING "id"', {})
        ],
    },
}


@patch.object(DatabaseService, "__init__", new=MagicMock(return_value=None))
@patch(f"{FILEPATH}.connect")
@parametrize(delete_tests)
def test_delete(
    mock_connect: MagicMock,
    id: int,
    expected_execute_calls: list[_Call],
) -> None:
    mock_execute: MagicMock = _mock_execute(mock_connect)
    DatabaseService().delete(id)
    mock_execute.assert_has_calls(expected_execute_calls)
