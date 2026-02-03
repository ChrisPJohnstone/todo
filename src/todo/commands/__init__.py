from . import (
    complete,
    count,
    create,
    delete,
    list_items,
    query,
    show,
    update,
)
from todo.constants import Commands
from todo.type_definitions import CommandModule


COMMANDS: dict[Commands, CommandModule] = {
    Commands.COMPLETE: complete,
    Commands.COUNT: count,
    Commands.CREATE: create,
    Commands.DELETE: delete,
    Commands.LIST: list_items,
    Commands.QUERY: query,
    Commands.SHOW: show,
    Commands.UPDATE: update,
}


__all__: list[str] = ["COMMANDS"]
