import sqlite3


class MyDBManager:

    def __init__(self, db_name: str, mode: str = "r"):
        self._db_name = db_name
        self._mode = mode
        self._connect = None
        self._cursor = None

    def __enter__(self):
        self._connect = sqlite3.connect(self._db_name)
        self._connect.row_factory = sqlite3.Row
        self._cursor = self._connect.cursor()
        return self._cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._mode == "w":
            self._connect.commit()
        self._connect.close()
