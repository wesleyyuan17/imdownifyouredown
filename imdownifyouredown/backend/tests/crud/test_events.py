from pathlib import Path
from sqlite3 import Connection

from imdownifyouredown.backend.crud.events import (
    get_event,
    insert_event,
    cancel_event,
    edit_event
)
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
        (1, 1, 2, 0),
        (1, 2, 0, 0),
        (1, 3, 2, 0),
        (2, 1, 2, 0),
        (2, 2, 3, 0),
        (3, 1, 0, 0),
        (3, 2, 1, 0),
        (3, 3, 2, 0),
        (3, 4, 3, 0)
    ]


def test_get_event(conn: Connection, tmp_path: Path):
    # conn fixture used to have same tmp_path to test db
    assert get_event(
        Event(1, [1, 2, 3]),
        (tmp_path / "test.db").absolute()
    ) == [(1, 'test1', [1, 2, 3], 1)]


def test_event_insertion(conn: Connection, tmp_path: Path):
    insert_event(
        Event(4, [3, 4]),
        (tmp_path / "test.db").absolute()
    )

    assert len(conn.execute("SELECT * FROM Events WHERE eventid = 4").fetchall()) > 0
    assert len(conn.execute("SELECT * FROM UserResponse WHERE eventid = 4").fetchall()) == 2
    user_info = conn.execute("SELECT * FROM UserInfo WHERE userid IN (3, 4)").fetchall()
    for user in user_info:
        assert 4 in user[2] # 2 is index of currentevents


def test_event_deletion(conn: Connection, tmp_path: Path):
    cancel_event(
        3,
        (tmp_path / "test.db").absolute()
    )

    assert len(conn.execute("SELECT * FROM Events WHERE eventid = 3").fetchall()) == 0
    assert len(conn.execute("SELECT * FROM UserResponse WHERE eventid = 3").fetchall()) == 0
    user_info = conn.execute("SELECT * FROM UserInfo").fetchall()
    for user in user_info:
        assert 3 not in user[2] # 2 is index of currentevents


def test_edit_event(conn: Connection, tmp_path: Path):
    edit_event(
        1,
        {"users": [1, 2, 3, 4]},
        (tmp_path / "test.db").absolute()
    )

    event = conn.execute("SELECT * FROM Events WHERE eventid = 1").fetchall()[0]
    assert event[2] == [1, 2, 3, 4]
