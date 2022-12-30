import os
import time
from pathlib import Path

class Variables():
    BASE_DIR = Path(__file__).resolve().parent

    #SQLITE
    SQLITE_NAME = f'test_sqlite.db'
    SQLITE_PATH = os.path.join(BASE_DIR, SQLITE_NAME)

variables = Variables()
