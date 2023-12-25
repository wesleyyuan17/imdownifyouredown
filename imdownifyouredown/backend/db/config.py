import json
import os
import sqlite3
from dataclasses import dataclass

DEFAULT_DB_NAME = "test.db"
DEFAULT_EVENTS_TABLE_NAME = "Events"
DEFAULT_USER_INFO_TABLE_NAME = "UserInfo"
DEFAULT_USER_PUBLIC_RESPONSE_TABLE_NAME = "UserPublicResponse"
DEFAULT_USER_PRIVATE_RESPONSE_TABLE_NAME = "UserPrivateResponse"


@dataclass(frozen=True)
class DBConfig:
    data_dir: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    db_name: str = os.path.join(data_dir, DEFAULT_DB_NAME)
    events_table: str = DEFAULT_EVENTS_TABLE_NAME
    user_info_table: str = DEFAULT_USER_INFO_TABLE_NAME
    user_public_response_table: str = DEFAULT_USER_PUBLIC_RESPONSE_TABLE_NAME
    user_private_response_table: str = DEFAULT_USER_PRIVATE_RESPONSE_TABLE_NAME
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


config = DBConfig(adapters=[adapt_list_to_json], converters=[convert_json_to_list])
# tests_config = DBConfig(
#     os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "test.db"),
#     adapters=[adapt_list_to_json],
#     converters=[convert_json_to_list]
# )
