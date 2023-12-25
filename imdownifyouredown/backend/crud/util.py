import json
import os
import sqlite3

from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum

from imdownifyouredown.backend.db.config import config

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


class EventResponse(Enum):
    NoResponse = 0
    Maybe = 1
    Down = 2
    NotDown = 3


@dataclass(frozen=True)
class User:
    user_id: int
    username: str


@dataclass(frozen=True)
class Event:
    event_id: int
    users: list[User]
    event_name: str | None = None
    live: bool = True


@dataclass(frozen=True)
class UserResponse:
    event_id: int
    user_id: int
    response: EventResponse
    

@contextmanager
def get_conn(db_name: str, read_only: bool=False) -> sqlite3.Connection:
    db_path = os.path.join(DATA_DIR, db_name)
    # acquire read/write lock with relevant permissions
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    try:
        yield conn
    finally:
        conn.close()


def generate_event_id():
    pass


def generate_user_id():
    pass
