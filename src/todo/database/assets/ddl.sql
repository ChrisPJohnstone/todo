CREATE TABLE IF NOT EXISTS "{table_name}" (
    "id"            INTEGER     PRIMARY KEY AUTOINCREMENT,
    "created_at"    TIMESTAMP   NOT NULL    DEFAULT CURRENT_TIMESTAMP,
    "message"       TEXT        NOT NULL,
    "due"           TIMESTAMP   NULL,
    "completed"     BOOLEAN     NOT NULL    DEFAULT 0,
    "completed_at"  TIMESTAMP   NULL
)
