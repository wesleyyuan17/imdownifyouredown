from imdownifyouredown.backend.crud.util import (
    Event,
    User,
    EventResponse,
    UserResponse,
    get_conn
)

DEFAULT_DB_NAME = "test.db"
DEFAULT_EVENTS_TABLE_NAME = "Events"
DEFAULT_USER_INFO_TABLE_NAME = "UserInfo"
DEFAULT_USER_RESPONSE_TABLE_NAME = "UserResponse"


def _resolve_db_table(ctx):
    pass


def get_event(
    event: Event,
    db_name: str | None = None
) -> list:
    db_name = db_name or DEFAULT_DB_NAME
    with get_conn(db_name) as conn:
        return conn.execute(
            "SELECT * FROM {} WHERE eventid = {}".format(
                DEFAULT_EVENTS_TABLE_NAME,
                event.event_id
            )
        ).fetchall()


def get_user(
    user: User,
    db_name: str | None = None
) -> list:
    db_name = db_name or DEFAULT_DB_NAME
    with get_conn(db_name) as conn:
        return conn.execute(
            "SELECT * FROM {} WHERE userid = {}".format(
                DEFAULT_USER_INFO_TABLE_NAME,
                user.user_id
            )
        ).fetchall()


def insert_event(
    event: Event,
    db_name: str | None = None
) -> None:
    db_name = db_name or DEFAULT_DB_NAME
    with get_conn(db_name) as conn:
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
            conn.execute(
                "DELETE FROM {} WHERE userid = {}".format(
                    DEFAULT_USER_INFO_TABLE_NAME,
                    userid
                )
            )
            sql = """
            INSERT INTO {} VALUES
                ({}, {}, {}, {})
            """.format(
                DEFAULT_USER_INFO_TABLE_NAME,
                userid,
                username,
                currentevents + [event.event_id],
                numpastevents + 1
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
    db_name: str | None = None
) -> None:
    db_name = db_name or DEFAULT_DB_NAME
    with get_conn(db_name) as conn:
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
            conn.execute(
                "DELETE FROM {} WHERE userid = {}".format(
                    DEFAULT_USER_INFO_TABLE_NAME,
                    userid
                )
            )
            sql = """
            INSERT INTO {} VALUES
                ({}, {}, {}, {})
            """.format(
                DEFAULT_USER_INFO_TABLE_NAME,
                userid,
                username,
                currentevents,
                numpastevents - 1
            )
            conn.execute(sql)

        conn.commit()


def insert_new_user(
    user: User,
    db_name: str | None = None
):
    db_name = db_name or DEFAULT_DB_NAME
    with get_conn(db_name) as conn:
        sql = "INSERT INTO {} VALUES\n({}, {}, {}, {})".format(
            user.user_id,
            user.username,
            [],
            0
        )
        conn.execute(sql)
        conn.commit()


def record_user_response(
    response: UserResponse,
    db_name: str | None = None
):
    db_name = db_name or DEFAULT_DB_NAME
    with get_conn(db_name) as conn:
        conn.execute(
            "DELETE FROM {} WHERE eventid = {eid} AND userid = {uid}".format(
                DEFAULT_USER_RESPONSE_TABLE_NAME,
                response.event_id,
                response.user_id
            )
        )
        sql = """
        INSERT INTO {} VALUES
            ({}, {}, {})
        """.format(
            DEFAULT_USER_RESPONSE_TABLE_NAME,
            response.event_id,
            response.user_id,
            response.response
        )
        conn.execute(sql)
        conn.commit()
