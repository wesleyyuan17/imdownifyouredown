from sqlite3 import Connection


def get_event(conn: Connection, event_id: str):
    return conn.execute(
        "SELECT * FROM events WHERE eventid = '{}'".format(
            event_id
        )
    )
