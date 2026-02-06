from enum import StrEnum


class Commands(StrEnum):
    COMPLETE = "complete"
    COUNT = "count"
    CREATE = "add"
    DELETE = "rm"
    LIST = "ls"
    QUERY = "query"
    SHOW = "show"
    TUI = "tui"
    UPDATE = "update"
