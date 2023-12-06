from sqlite3 import Connection

from imdownifyouredown.backend.crud.events import get_event, get_user_events
from imdownifyouredown.backend.crud.util import Event, User


def test_db_read_write(conn: Connection):
    pass
