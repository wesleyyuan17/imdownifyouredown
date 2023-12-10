from pathlib import Path
from sqlite3 import Connection

from imdownifyouredown.backend.crud.events import get_event
from imdownifyouredown.backend.crud.util import Event, User


def test_db_read(conn: Connection):
    events_results = conn.execute("SELECT * FROM Events").fetchall()
    assert events_results == [
        (1, 'test1', [1, 2, 3], 1),
        (2, 'test2', [1, 2], 0),
        (3, 'test3', [1, 2, 3, 4], 1)
    ]
    user_info_results = conn.execute("SELECT * FROM UserInfo").fetchall()
    assert user_info_results == [
        (1, 'user1', [1, 2, 3], 3),
        (2, 'user2', [1, 2, 3], 3),
        (3, 'user3', [1, 3], 2),
        (4, 'user4', [3], 1)
    ]
    user_response_results = conn.execute("SELECT * FROM UserResponse").fetchall()
    assert user_response_results == [
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


def test_get_event(conn: Connection, tmp_path: Path):
    print(conn.execute("PRAGMA database_list").fetchall())
    print("in test", (tmp_path / "test.db").absolute())
    assert get_event(
        Event(1, [1, 2, 3]),
        (tmp_path / "test.db").absolute()
    ) == [(1, 'test1', [1, 2, 3], 1)]


def test_get_user():
    pass


def test_event_insertion(conn: Connection):
    pass


def test_event_deletion(conn: Connection):
    pass


def test_enter_user_response(conn: Connection):
    pass
