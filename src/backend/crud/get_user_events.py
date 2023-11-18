from sqlite3 import Connection


def get_user_events(conn: Connection, user_id: str):
    return conn.execute(
        "SELECT * FROM events WHERE user_id = '{}'".format(
            user_id
        )
    )