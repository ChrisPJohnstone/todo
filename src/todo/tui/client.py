from curses import window, wrapper

from todo.database import DatabaseClient


class TUI:
    def __init__(
        self,
        database_client: DatabaseClient,
    ) -> None:
        # TODO: Add logging
        self.database_client: DatabaseClient = database_client
        wrapper(self.main)

    @property
    def database_client(self) -> DatabaseClient:
        """Database client used by TUI"""
        return self._database_client

    @database_client.setter
    def database_client(self, value: DatabaseClient) -> None:
        self._database_client: DatabaseClient = value

    def main(self, stdscr: window) -> None:
        """
        Main Processing Loop For TUI

        Args:
            stdscr (window): curses window to display on
        """
        pass
