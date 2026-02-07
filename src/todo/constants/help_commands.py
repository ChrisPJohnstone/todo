from .enum_commands import Commands


HELP_COMMANDS: dict[Commands, str] = {
    Commands.COMPLETE: "Mark an item as completed",
    Commands.COUNT: "Get a count of items",
    Commands.CREATE: "Add a new item",
    Commands.DELETE: "Remove an item",
    Commands.LIST: "List all items",
    Commands.QUERY: "Query table directly with SQL",
    Commands.SHOW: "Show details of an item",
    Commands.TUI: "Launch TUI",
    Commands.UPDATE: "Update an existing item",
}
