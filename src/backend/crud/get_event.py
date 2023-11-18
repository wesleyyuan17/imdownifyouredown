from sqlite3 import Connection


def get_event(conn: Connection, event_id: str):
    return conn.execute(
        "SELECT * FROM events WHERE event_id = '{}'".format(
            event_id
        )
    )
