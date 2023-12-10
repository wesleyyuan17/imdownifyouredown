import os
import sqlite3

from dataclasses import dataclass
from enum import Enum

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


@dataclass(frozen=True)
class UserResponse:
    event_id: int
    user_id: int
    response: EventResponse


def get_conn(db_name: str) -> sqlite3.Connection:
    db_path = os.path.join(DATA_DIR, f"{db_name}.db")
    return sqlite3.connect(db_path)


def generate_event_id():
    pass


def generate_user_id():
    pass
