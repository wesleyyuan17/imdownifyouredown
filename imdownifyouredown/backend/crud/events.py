from imdownifyouredown.backend.crud.util import (
    Event,
    User,
    EventResponse,
    UserResponse,
    get_conn
)

DEFAULT_DB_NAME = "test"
DEFAULT_EVENTS_TABLE_NAME = "Events"
DEFAULT_USER_INFO_TABLE_NAME = "UserInfo"
DEFAULT_USER_RESPONSE_TABLE_NAME = "UserResponse"


def _resolve_db_table(ctx):
    pass


def get_event(
    event: Event,
) -> list:
    conn = get_conn(DEFAULT_DB_NAME)
    
    return conn.execute(
        "SELECT * FROM {} WHERE eventid = {}".format(
            DEFAULT_EVENTS_TABLE_NAME,
            event.event_id
        )
    ).fetchall()


def get_user_events(
    user: User,
) -> list:
    conn = get_conn(DEFAULT_DB_NAME)
    
    return conn.execute(
        "SELECT * FROM {} WHERE userid = {}".format(
            DEFAULT_USER_INFO_TABLE_NAME,
            user.user_id
        )
    ).fetchall()


def record_user_response(
    response: UserResponse,
):
    conn = get_conn(DEFAULT_DB_NAME)
    sql = """
    DELETE FROM {tbl} WHERE eventid = {eid} AND userid = {uid};
    INSERT INTO {tbl} VALUES
        ({eid}, {uid}, {})
    """.format(
        response.response,
        tbl=DEFAULT_USER_RESPONSE_TABLE_NAME,
        eid=response.event_id,
        uid=response.user_id
    )
    conn.execute(sql)
    conn.commit()


def insert_event(
    event: Event,
) -> None:
    conn = get_conn(DEFAULT_DB_NAME)

    # insert event into events table
    sql = "INSERT INTO {} VALUES\n({}, {}, {}, {})".format(
        DEFAULT_EVENTS_TABLE_NAME,
        event.event_id,
        event.event_name,
        event.users,
        True
    )
    conn.execute(sql)

    # add event to users, initialize responses
    sql = "SELECT * FROM {} WHERE userid IN {}".format(
        DEFAULT_USER_INFO_TABLE_NAME,
        event.users
    )
    user_info = conn.execute(sql).fetchall()
    for ui in user_info:
        userid, username, currentevents, numpastevents = ui
        sql = """
        DELETE FROM {tbl} WHERE userid = {uid};
        INSERT INTO {tbl} VALUES
            ({uid}, {}, {}, {})
        """.format(
            username,
            currentevents + [event.event_id],
            numpastevents + 1,
            tbl=DEFAULT_USER_INFO_TABLE_NAME,
            uid=userid
        )
        conn.execute(sql)

    for user in event.users:
        sql = "INSERT INTO {} VALUES\n({}, {}, {})".format(
            DEFAULT_USER_RESPONSE_TABLE_NAME,
            event.event_id,
            user,
            EventResponse.NoResponse
        )
        conn.execute(sql)
    
    conn.commit()


def cancel_event(
    event: Event,
) -> None:
    conn = get_conn(DEFAULT_DB_NAME)

    # remove event from event/response tables
    for tbl in [DEFAULT_EVENTS_TABLE_NAME, DEFAULT_USER_RESPONSE_TABLE_NAME]:
        sql = "DELETE FROM {} WHERE eventid = {}".format(tbl, event.event_id)
        conn.execute(sql)

    # remove event from current events of users
    sql = "SELECT * FROM {} WHERE userid IN {}".format(
        DEFAULT_USER_INFO_TABLE_NAME,
        event.users
    )
    user_info = conn.execute(sql).fetchall()
    for ui in user_info:
        userid, username, currentevents, numpastevents = ui
        currentevents.remove(event.event_id)
        sql = """
        DELETE FROM {tbl} WHERE userid = {uid};
        INSERT INTO {tbl} VALUES
            ({uid}, {}, {}, {})
        """.format(
            username,
            currentevents,
            numpastevents - 1,
            tbl=DEFAULT_USER_INFO_TABLE_NAME,
            uid=userid
        )
        conn.execute(sql)

    conn.commit()
