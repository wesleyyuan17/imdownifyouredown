from imdownifyouredown.backend.crud.util import (
    User,
    UserResponse,
    get_conn
)
from imdownifyouredown.backend.db.config import config


def get_user(
    user: User,
    db_name: str | None = None
) -> list:
    db_name = db_name or config.db_name
    with get_conn(db_name) as conn:
        return conn.execute(
            "SELECT * FROM {} WHERE userid = {}".format(
                config.user_info_table,
                user.user_id
            )
        ).fetchall()


def insert_new_user(
    user: User,
    db_name: str | None = None
):
    db_name = db_name or config.db_name
    with get_conn(db_name) as conn:
        conn.executemany(
            f"INSERT INTO {config.user_info_table} VALUES (?, ?, ?, ?)",
            [
                (user.user_id, user.username, [], 0)
            ]
        )
        conn.commit()


def record_user_response(
    response: UserResponse,
    db_name: str | None = None
):
    db_name = db_name or config.db_name
    with get_conn(db_name) as conn:
        conn.execute(
            "DELETE FROM {} WHERE eventid = {} AND userid = {}".format(
                config.user_response_table,
                response.event_id,
                response.user_id
            )
        )
        conn.executemany(
            f"INSERT INTO {config.user_response_table} VALUES (?, ?, ?, ?)",
            [
                (response.event_id, response.user_id, response.public_response, response.private_response)
            ]
        )
        conn.commit()



