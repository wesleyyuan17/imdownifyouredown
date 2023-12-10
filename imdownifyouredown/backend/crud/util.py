import json
import os
import sqlite3

from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum

from imdownifyouredown.backend.db.config import DEFAULT_CONFIG

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DEFAULT_DB_NAME = "test.db"
DEFAULT_EVENTS_TABLE_NAME = "Events"
DEFAULT_USER_INFO_TABLE_NAME = "UserInfo"
DEFAULT_USER_RESPONSE_TABLE_NAME = "UserResponse"


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


def adapt_list_to_json(l: list):
    return json.dumps(l).encode("utf-8")


def convert_json_to_list(data: object):
    return json.loads(data.decode("utf-8"))


sqlite3.register_adapter(list, adapt_list_to_json)
sqlite3.register_converter("json", convert_json_to_list)
    

@contextmanager
def get_conn(db_name: str) -> sqlite3.Connection:
    db_path = os.path.join(DATA_DIR, db_name)
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    try:
        yield conn
    finally:
        conn.close()


def generate_event_id():
    pass


def generate_user_id():
    pass
