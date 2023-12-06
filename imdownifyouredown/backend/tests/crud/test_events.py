import os
import sqlite3

from imdownifyouredown.backend.crud.events import get_event, get_user_events
from imdownifyouredown.backend.crud.util import Event, User


def test_db_read_write():
    file_dir = os.path.dirname(__file__)
    test_db_path = os.path.join(os.path.dirname(file_dir), "data", "test.db")
    conn = sqlite3.connect(test_db_path)
    conn.execute("DROP TABLE IF EXISTS Events")
    conn.execute("CREATE TABLE IF NOT EXISTS Events(eventid, userid, eventname, down)")
    conn.execute(
        """
        INSERT INTO Events VALUES
            (1, 1, 'test1', True),
            (1, 2, 'test1', False),
            (2, 1, 'test2', True)
        """
    )
    conn.commit()
    assert get_event(Event(1, [User(1, "foo")])) == [(1, 1, 'test1', 1), (1, 2, 'test1', 0)]
    assert get_event(Event(2, [User(1, "foo")])) == [(2, 1, 'test2', 1)]
    assert get_user_events(User(1, "foo")) == [(1, 1, 'test1', 1), (2, 1, 'test2', 1)]

    conn.close()