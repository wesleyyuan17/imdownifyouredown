import os
import sqlite3

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def get_conn(db_name: str) -> sqlite3.Connection:
    db_path = os.path.join(DATA_DIR, f"{db_name}.db")
    return sqlite3.connect(db_path)
