from curses import A_NORMAL, A_REVERSE, newwin, window
from curses.textpad import Textbox
from logging import DEBUG, Logger, getLogger
from textwrap import wrap

from ..constants import Action, Key
from ..item import Item
from ..type_definitions import Bindings
from ..utils import message_box, textbox_validator
from ._base import WinBase
from todo.database import DatabaseClient


class WinItem(WinBase):
    def __init__(
        self,
        database_client: DatabaseClient,
        item: Item,
        x_strt: int = 0,
        y_strt: int = 0,
        x_len_max: int = 0,
        y_len_max: int = 0,
        logger: Logger = getLogger(__name__),
    ) -> None:
        super().__init__(
            database_client=database_client,
            x_strt=x_strt,
            y_strt=y_strt,
            x_len_max=x_len_max,
            y_len_max=y_len_max,
            logger=logger,
        )
        self.item = item
        self.index_current = 0

    @property
    def BINDINGS(self) -> Bindings:
        return {
            Key.CTRL_J: Action.ENTER,
            Key.CTRL_M: Action.ENTER,
            Key.ENTER: Action.ENTER,
            Key.L_J: Action.DOWN,
            Key.L_K: Action.UP,
            Key.L_Q: Action.QUIT,
        }

    @property
    def item(self) -> Item:
        return self._items

    @item.setter
    def item(self, value: Item) -> None:
        self._log(DEBUG, f"Setting item to {value}")
        self._items: Item = value

    @property
    def fields(self) -> dict[str, str]:
        return {
            "Created At": self.item.created_at,
            "Due": self.item.due,
            "Completed": str(bool(self.item.completed)),
            "Message": self.item.message,
        }

    @property
    def n_fields(self) -> int:
        return len(self.fields)

    @property
    def index_max(self) -> int:
        return self.n_fields - 1

    @property
    def index_current(self) -> int:
        return self._index_current

    @index_current.setter
    def index_current(self, value: int) -> None:
        self._log(DEBUG, f"Setting index current to {value}")
        if value < 0 or value > self.index_max:
            value = value % self.n_fields
        self._index_current: int = value

    @property
    def current_field(self) -> str:
        return list(self.fields.keys())[self.index_current]

    @staticmethod
    def _message(message: str) -> str:
        return f"Item Window: {message}"

    def init_win(self) -> None:
        self._win = newwin(
            self.y_len,  # nlines
            self.x_len,  # ncols
            self.y_strt,  # begin_y
            self.x_strt,  # begin_x
        )

    def refresh_item(self) -> None:
        self._log(DEBUG, f"Reloading item with id {self.item.id}")
        criteria: str = f"WHERE id = {self.item.id}"
        item_data: list[tuple] = self.database_client.get_list(criteria)
        if len(item_data) != 2:
            raise ValueError(f"Expected 1 item, got {len(item_data) - 1}")
        self.item = Item(*item_data[1])

    def _message_box(
        self,
        win: window,
        title: str,
        message: str,
        title_attr: int,
        x_strt: int = 0,
        y_strt: int = 0,
    ) -> None:
        message_box(
            win=win,
            x_strt=x_strt,
            y_strt=y_strt,
            x_stop=self.x_len - 3,
            y_max=self.y_len - 1,
            title=title,
            message=message,
            title_attr=title_attr,
        )

    def _draw(self) -> None:
        self._log(DEBUG, "Drawing")
        for index, title in enumerate(self.fields):
            if index == self.index_current:
                title_attr: int = A_REVERSE
            else:
                title_attr: int = A_NORMAL
            self._message_box(
                win=self._win,
                title=title,
                message=self.fields[title],
                y_strt=index * 3,
                title_attr=title_attr,
            )
        self._win.refresh()

    def _edit_field(self) -> None:
        self._log(DEBUG, f"Editing field {self.current_field}")
        value: str = self.fields[self.current_field]
        text_win: window = newwin(
            len(wrap(value, self.x_len - 3)),
            self.x_len - 4,
            self.y_strt + self.index_current * 3 + 1,
            self.x_strt + 1,
        )
        text_win.addstr(0, 0, value)
        text_win.refresh()
        text_box: Textbox = Textbox(text_win)
        text_box.edit(textbox_validator)
        new_value: str = text_box.gather().strip()
        self._log(DEBUG, f"New value for {self.current_field} is {new_value}")
        db_field: str = self.current_field.lower().replace(" ", "_")
        self.update_item(self.item.id, {db_field: new_value})
        self.refresh_item()

    def action(self, action: Action, windows: list[WinBase]) -> None:
        match action:
            case Action.QUIT:
                windows.pop(0)
                windows[0].refresh_items()  # type: ignore
                # TODO: Make more generic by adding a refresh method to WinBase and calling that instead
            case Action.DOWN:
                self.index_current += 1
            case Action.UP:
                self.index_current -= 1
            case Action.ENTER:
                self._edit_field()
