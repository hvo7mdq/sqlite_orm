"""
@ARTHUR:rkp
"""
from sqliteorm.sqlite_base import SqliteClient,sqlite

class SqliteBackendBase():
    """not implemented"""
    def __init__(
        self,
        db_path=None,
        ) -> None:
        self.db_path = db_path

    @property
    def get_db(self):
        if self.db_path:
            db = SqliteClient(db_path=self.db_path,conn=None)
        else:
            db = sqlite
        return db