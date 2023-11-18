from imdownifyouredown.backend.crud.util import get_conn

DEFAULT_DB_NAME = "test"
DEFAULT_TABLE_NAME = "Events"


def get_event(
    event_id: str,
    db_name: str | None = None,
    table_name: str | None = None
):
    conn = get_conn(db_name)

    if db_name is None:
        db_name = DEFAULT_DB_NAME
    if table_name is None:
        table_name = DEFAULT_TABLE_NAME
    
    return conn.execute(
        "SELECT * FROM {} WHERE eventid = {}".format(
            table_name,
            event_id
        )
    ).fetchall()


def get_user_events(
    user_id: str,
    db_name: str | None = None,
    table_name: str | None = None
):
    conn = get_conn(db_name)

    if db_name is None:
        db_name = DEFAULT_DB_NAME
    if table_name is None:
        table_name = DEFAULT_TABLE_NAME
    
    return conn.execute(
        "SELECT * FROM {} WHERE userid = {}".format(
            table_name,
            user_id
        )
    ).fetchall()


def insert_event(
    event_id: str,
    event_params: dict[str, str],
    db_name: str | None = None,
    table_name: str | None = None
):
    conn = get_conn(db_name)

    if db_name is None:
        db_name = DEFAULT_DB_NAME
    if table_name is None:
        table_name = DEFAULT_TABLE_NAME
    
    sql = "INSERT INTO {} VALUES".format(table_name)
    for uid in event_params["user_ids"]:
        sql += "\n({}, {}, {}, {})".format(
            event_id,
            uid,
            event_params.get("eventname", None),
            True
        )
        sql += ","

    conn.execute(sql)
