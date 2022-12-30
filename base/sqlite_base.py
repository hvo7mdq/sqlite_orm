import sqlite3
from sqlite_orm.base.variables import variables


class SqliteClient():
    def __init__(self, db_path=None, conn=None) -> None:
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = variables.SQLITE_PATH

    def __call__(self):
        # TODO: connection error handle
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        self.conn = conn
        return self

sqlite = SqliteClient()

