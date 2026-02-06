INSERT INTO "{table_name}" ("message", "due")
VALUES (:message, :due)
RETURNING "id"
