import sqlite3

from imdownifyouredown.backend.crud.events import get_event, get_user_events


if __name__ == "__main__":
    conn = sqlite3.connect("backend/data/test.db")
    conn.execute("CREATE TABLE IF NOT EXISTS Events(eventid, userid, eventname, down)")
    conn.execute(
        """
        INSERT INTO Events VALUES
            (1, 1, 'test1', True),
            (1, 2, 'test1', False),
            (2, 1, 'test2', True)
        """
    )
    print(
        get_event(conn, 1),
        get_event(conn, 2),
        get_user_events(conn, 1),
        sep="\n"
    )
    conn.close()
