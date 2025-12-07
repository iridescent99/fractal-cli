from pathlib import Path
from fractalcli.database import DatabaseHandler


class FractalTaskEngine:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)
