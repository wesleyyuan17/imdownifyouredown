import json
import sqlite3
from dataclasses import dataclass

DEFAULT_DB_NAME = "test.db"
DEFAULT_EVENTS_TABLE_NAME = "Events"
DEFAULT_USER_INFO_TABLE_NAME = "UserInfo"
DEFAULT_USER_RESPONSE_TABLE_NAME = "UserResponse"


@dataclass(frozen=True)
class DBConfig:
    db_name:  str
    db_name: str = DEFAULT_DB_NAME
    events_table: str = DEFAULT_EVENTS_TABLE_NAME
    user_info_table: str = DEFAULT_USER_INFO_TABLE_NAME
    user_response_table: str = DEFAULT_USER_RESPONSE_TABLE_NAME
    adapters: list[callable] | None = None
    converters: list[callable] | None = None

    def __post_init__(self):
        for adf in self.adapters:
            sqlite3.register_adapter(list, adf)
        for convf in self.converters:
            sqlite3.register_converter("json", convf)


def adapt_list_to_json(l: list):
    return json.dumps(l).encode("utf-8")


def convert_json_to_list(data: object):
    return json.loads(data.decode("utf-8"))


config = DBConfig("test", [adapt_list_to_json], [convert_json_to_list])
