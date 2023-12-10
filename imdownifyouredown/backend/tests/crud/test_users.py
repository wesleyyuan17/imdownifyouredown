from pathlib import Path
from sqlite3 import Connection

from imdownifyouredown.backend.crud.users import insert_new_user, record_user_response
from imdownifyouredown.backend.crud.util import User, UserResponse


def test_user_insertion(conn: Connection, tmp_path: Path):
    insert_new_user(
        User(5, "test5"),
        (tmp_path / "test.db").absolute()
    )

    assert len(conn.execute("SELECT * FROM UserInfo WHERE userid = 5").fetchall()) == 1


def test_record_user_response(conn: Connection, tmp_path: Path):
    record_user_response(
        UserResponse(1, 1, 3),
        (tmp_path / "test.db").absolute()
    )

    result = conn.execute("SELECT * FROM UserResponse WHERE eventid = 1 AND userid = 1").fetchall()
    assert result[0][2] == 3
