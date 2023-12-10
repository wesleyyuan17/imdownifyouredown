from imdownifyouredown.backend.crud.util import (
    DEFAULT_DB_NAME,
    DEFAULT_USER_RESPONSE_TABLE_NAME,
    User,
    UserResponse,
    get_conn
)


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