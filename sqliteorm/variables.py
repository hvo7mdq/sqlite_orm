"""
@ARTHUR:rkp
"""
import os
from pathlib import Path

class Variables():
    BASE_DIR = Path(__file__).resolve().parent

    #SQLITE
    SQLITE_BACKEND = 'sqliteorm.sqlite_backend.SqliteBackendBase.get_db'
    SQLITE_NAME = f'test_sqlite.db'
    SQLITE_PATH = os.path.join(BASE_DIR, SQLITE_NAME)

variables = Variables()
