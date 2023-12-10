import pytest

import sqlite3
from pathlib import Path

from imdownifyouredown.backend.crud.util import adapt_list_to_json, convert_json_to_list
sqlite3.register_adapter(list, adapt_list_to_json)
sqlite3.register_converter("json", convert_json_to_list)


@pytest.fixture
def conn(tmp_path: Path):
    test_db_path = tmp_path / "test.db"
    conn = sqlite3.connect(test_db_path.absolute(), detect_types=sqlite3.PARSE_DECLTYPES)

    conn.execute("DROP TABLE IF EXISTS Events")
    conn.execute("DROP TABLE IF EXISTS UserInfo")
    conn.execute("DROP TABLE IF EXISTS UserResponse")
    conn.execute("CREATE TABLE IF NOT EXISTS Events(eventid PRIMARY KEY, eventname, users json, down)")
    conn.execute("CREATE TABLE IF NOT EXISTS UserInfo(userid PRIMARY KEY, username, currentevents json, numpastevents)")
    conn.execute("CREATE TABLE IF NOT EXISTS UserResponse(eventid, userid, down, PRIMARY KEY (eventid, userid))")
    conn.executemany(
        "INSERT INTO Events VALUES (?, ?, ?, ?)",
        [
            (1, 'test1', [1, 2, 3], True),
            (2, 'test2', [1, 2], False),
            (3, 'test3', [1, 2, 3, 4], True)
        ]
    )
    conn.executemany(
        "INSERT INTO UserInfo VALUES (?, ?, ?, ?)",
        [
            (1, 'user1', [1, 2, 3], 3),
            (2, 'user2', [1, 2, 3], 3),
            (3, 'user3', [1, 3], 2),
            (4, 'user4', [3], 1)
        ]
    )
    conn.executemany(
        "INSERT INTO UserResponse VALUES (?, ?, ?)",
        [
            (1, 1, 2),
            (1, 2, 0),
            (1, 3, 2),
            (2, 1, 2),
            (2, 2, 3),
            (3, 1, 0),
            (3, 2, 1),
            (3, 3, 2),
            (3, 4, 3)
        ]
    )
    conn.commit()

    return conn

