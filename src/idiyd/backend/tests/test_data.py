import sqlite3

from backend.crud.get_event import get_event
from backend.crud.get_user_events import get_user_events


if __name__ == "__main__":
    conn = sqlite3.connect("backend/data/test.db")
    # conn.execute("CREATE TABLE events(eventid, userid, eventname, username, down)")
    # conn.execute(
    #     """
    #     INSERT INTO events VALUES
    #         (1, 1, 'test1', 'foo', True),
    #         (1, 2, 'test1', 'bar', False),
    #         (2, 1, 'test2', 'foo', True)
    #     """
    # )
    print(
        get_event(conn, 1),
        get_event(conn, 2),
        get_user_events(conn, 1),
        sep="\n"
    )
    conn.close()
