import json
import sqlite3
from dataclasses import dataclass

@dataclass(frozen=True)
class DBConfig:
    db_name:  str
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


DEFAULT_CONFIG = DBConfig("test", [adapt_list_to_json], [convert_json_to_list])
