"""
Kate Yurmanovych
Lesson 7 Task 1
1) Написать контекстный менеджер для работы с SQLite DB.
"""
import sqlite3


class MyDBManager:

    def __init__(self, db_name:str):
        self._db_name = db_name
        self._connect = None
        self._cursor = None

    def __enter__(self):
        self._connect = sqlite3.connect(self._db_name)
        self._cursor = self._connect.cursor()
        return self._cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connect.commit()
        self._connect.close()


if __name__ == "__main__":
    with MyDBManager("sqllite_db.bd") as bd:
        query = bd.execute("SELECT * FROM person")
        print("Test query:", query.fetchall())
