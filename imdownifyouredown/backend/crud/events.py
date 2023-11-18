from imdownifyouredown.backend.crud.util import Event, User, get_conn

DEFAULT_DB_NAME = "test"
DEFAULT_TABLE_NAME = "Events"


def get_event(
    event: Event,
    db_name: str | None = None,
    table_name: str | None = None
) -> list:
    if db_name is None:
        db_name = DEFAULT_DB_NAME
    if table_name is None:
        table_name = DEFAULT_TABLE_NAME

    conn = get_conn(db_name)
    
    return conn.execute(
        "SELECT * FROM {} WHERE eventid = {}".format(
            table_name,
            event.event_id
        )
    ).fetchall()


def get_user_events(
    user: User,
    db_name: str | None = None,
    table_name: str | None = None
) -> list:
    if db_name is None:
        db_name = DEFAULT_DB_NAME
    if table_name is None:
        table_name = DEFAULT_TABLE_NAME

    conn = get_conn(db_name)
    
    return conn.execute(
        "SELECT * FROM {} WHERE userid = {}".format(
            table_name,
            user.user_id
        )
    ).fetchall()


def insert_event(
    event: Event,
    db_name: str | None = None,
    table_name: str | None = None
) -> None:
    if db_name is None:
        db_name = DEFAULT_DB_NAME
    if table_name is None:
        table_name = DEFAULT_TABLE_NAME

    conn = get_conn(db_name)
    
    sql = "INSERT INTO {} VALUES".format(table_name)
    for user in event.users:
        sql += "\n({}, {}, {}, {})".format(
            event.event_id,
            user.user_id,
            event.event_name,
            True
        )
        sql += ","

    conn.execute(sql)
    conn.commit()
