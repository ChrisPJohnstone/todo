# ToDo CLI

## Overview

CLI app to manage todo list written in Python standard library.
- Stores items in a SQLite database
- All commands will initiate a daemon (overwriting if already exists) which will send system notifications when notifications are due.
    - Only works for MacOS and Linux, I don't care about Windows

## Usage

- `td --help` will show you all the up date options for using the tool
- `td add` creates a todo item. Example `td add do the dishes`
- `td complete [id]` completes a todo item
- `td count` gives you a count of todo items. Optional filtering example `td count id > 5`
- `td rm [id]` deletes a todo item
- `td ls` lists todo items. Optional filtering example `td ls id > 5`
- `td query` enables freely querying the todo table. Example `td query TRUNCATE TABLE todo;`
- `td show [id]` shows a specific todo item
- `td update [id]` updates a todo item. Change due date example `td updaet 3 --due monday`

## Development

- You can run without install by calling dir e.g. `python src/todo/`

## TMUX Integration

You can use widgets (e.g. `#(while td count; do sleep 5; done)`) to include td items in your status bar.
