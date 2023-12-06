from sqlite3 import Connection

from imdownifyouredown.backend.crud.events import get_event, get_user_events
from imdownifyouredown.backend.crud.util import Event, User


def test_db_read_write(conn: Connection):
    assert get_event(Event(1, [User(1, "foo")])) == [(1, 1, 'test1', 1), (1, 2, 'test1', 0)]
    assert get_event(Event(2, [User(1, "foo")])) == [(2, 1, 'test2', 1)]
    assert get_user_events(User(1, "foo")) == [(1, 1, 'test1', 1), (2, 1, 'test2', 1)]
