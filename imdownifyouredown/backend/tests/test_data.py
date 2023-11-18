import os
import sqlite3

from imdownifyouredown.backend.crud.events import get_event, get_user_events
from imdownifyouredown.backend.crud.util import Event, User


if __name__ == "__main__":
    file_dir = os.path.dirname(__file__)
    test_db_path = os.path.join(os.path.dirname(file_dir), "data", "test.db")
    conn = sqlite3.connect(test_db_path)
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
    print(
        get_event(Event(1, [User(1, "foo")])),
        get_event(Event(2, [User(1, "foo")])),
        get_user_events(User(1, "foo")),
        sep="\n"
    )
    conn.close()
