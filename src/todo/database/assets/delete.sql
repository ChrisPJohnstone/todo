DELETE FROM "{table_name}"
WHERE "id" = {{id}}
RETURNING "id"
