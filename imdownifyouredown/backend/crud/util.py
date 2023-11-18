import os
import sqlite3

from dataclasses import dataclass

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


@dataclass(frozen=True)
class User:
    user_id: int
    username: str


@dataclass(frozen=True)
class Event:
    event_id: int
    users: list[User]
    event_name: str | None = None


def get_conn(db_name: str) -> sqlite3.Connection:
    db_path = os.path.join(DATA_DIR, f"{db_name}.db")
    return sqlite3.connect(db_path)


def generate_event_id():
    pass


def generate_user_id():
    pass
