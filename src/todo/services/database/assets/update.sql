UPDATE "{table_name}"
SET {{fields}}
WHERE "id" = {{id}}
RETURNING "id"
