import configparser
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
import json

from fractalcli import DB_WRITE_ERROR, SUCCESS, DB_READ_ERROR, JSON_ERROR

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_todo.json"
)


class DBResponse(NamedTuple):
    todo_list: List[Dict[str, Any]]
    error: int


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the to-do database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    """Create the to-do database."""
    try:
        db_path.write_text(json.dumps({"tasks": []}))  # Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_tasks(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse([], JSON_ERROR)
        except OSError:  # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)

    def write_tasks(self, task_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(task_list, db, indent=4)
            return DBResponse(task_list, SUCCESS)
        except OSError:  # Catch file IO problems
            return DBResponse(task_list, DB_WRITE_ERROR)
