from .base import Command
from .complete import Complete
from .count import Count
from .create import Create
from .delete import Delete
from .list import List
from .query import Query
from .show import Show
from .update import Update


COMMAND_DICT: dict[str, type[Command]] = {
    "add": Create,
    "complete": Complete,
    "count": Count,
    "rm": Delete,
    "ls": List,
    "query": Query,
    "show": Show,
    "update": Update,
}
