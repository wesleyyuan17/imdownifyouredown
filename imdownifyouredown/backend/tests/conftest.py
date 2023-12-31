import pytest

import sqlite3
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from imdownifyouredown.backend.api import api_router
from imdownifyouredown.backend.db.config import adapt_list_to_json, convert_json_to_list
sqlite3.register_adapter(list, adapt_list_to_json)
sqlite3.register_converter("json", convert_json_to_list)


@pytest.fixture
def conn(tmp_path: Path):
    test_db_path = tmp_path / "test.db"
    conn = sqlite3.connect(test_db_path.absolute(), detect_types=sqlite3.PARSE_DECLTYPES)

    conn.execute("DROP TABLE IF EXISTS Events")
    conn.execute("DROP TABLE IF EXISTS UserInfo")
    conn.execute("DROP TABLE IF EXISTS UserPublicResponse")
    conn.execute("DROP TABLE IF EXISTS UserPrivateResponse")
    conn.execute("CREATE TABLE IF NOT EXISTS Events(eventid PRIMARY KEY, eventname, users json, live)")
    conn.execute("CREATE TABLE IF NOT EXISTS UserInfo(userid PRIMARY KEY, username, currentevents json, numpastevents)")
    conn.execute("CREATE TABLE IF NOT EXISTS UserPublicResponse(eventid, userid, down, PRIMARY KEY (eventid, userid))")
    conn.execute("CREATE TABLE IF NOT EXISTS UserPrivateResponse(eventid, userid, down, PRIMARY KEY (eventid, userid))")
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
        "INSERT INTO UserPublicResponse VALUES (?, ?, ?)",
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
    conn.executemany(
        "INSERT INTO UserPrivateResponse VALUES (?, ?, ?)",
        [
            (1, 1, 0),
            (1, 2, 0),
            (1, 3, 0),
            (2, 1, 0),
            (2, 2, 0),
            (3, 1, 0),
            (3, 2, 0),
            (3, 3, 0),
            (3, 4, 0)
        ]
    )
    conn.commit()

    return conn


@pytest.fixture
def client(conn: sqlite3.Connection):
    app = FastAPI()
    app.include_router(api_router)

    return TestClient(app)
