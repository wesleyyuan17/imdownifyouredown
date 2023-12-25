from imdownifyouredown.backend.crud.events import cancel_event
from imdownifyouredown.backend.crud.notifications import notify_cancel
from imdownifyouredown.backend.crud.util import (
    EventResponse,
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
    with get_conn(db_name, read_only=True) as conn:
        return conn.execute(
            "SELECT * FROM {} WHERE userid = {}".format(
                config.user_info_table,
                user.user_id
            )
        ).fetchall()


def insert_new_user(
    user: User,
    db_name: str | None = None
) -> None:
    db_name = db_name or config.db_name
    with get_conn(db_name) as conn:
        conn.executemany(
            f"INSERT INTO {config.user_info_table} VALUES (?, ?, ?, ?)",
            [
                (user.user_id, user.username, [], 0)
            ]
        )
        conn.commit()


def record_user_public_response(
    response: UserResponse,
    db_name: str | None = None
) -> None:
    db_name = db_name or config.db_name
    with get_conn(db_name) as conn:
        conn.execute(
            "DELETE FROM {} WHERE eventid = {} AND userid = {}".format(
                config.user_public_response_table,
                response.event_id,
                response.user_id
            )
        )
        conn.executemany(
            f"INSERT INTO {config.user_public_response_table} VALUES (?, ?, ?)",
            [
                (response.event_id, response.user_id, response.response)
            ]
        )

        conn.commit()


def record_user_private_response(
    response: UserResponse,
    db_name: str | None = None
) -> None:
    def resolve_responses(event_responses: list) -> bool:
        """
        Helper function that determines whether an event should be cancelled. Returns
        True if cancelled, False if still on.

        Will handle conditional responses in the future, for now only cancel if all
        indicate not down.
        """
        return all([r[0] == EventResponse.NotDown.value for r in event_responses])
    
    db_name = db_name or config.db_name
    with get_conn(db_name) as conn:
        conn.execute(
            "DELETE FROM {} WHERE eventid = {} AND userid = {}".format(
                config.user_public_response_table,
                response.event_id,
                response.user_id
            )
        )
        conn.executemany(
            f"INSERT INTO {config.user_public_response_table} VALUES (?, ?, ?)",
            [
                (response.event_id, response.user_id, response.response)
            ]
        )

        # check if all privately not down in which case, cancel event
        event_responses = conn.execute(
            "SELECT down FROM {} WHERE eventid = {}".format(
                config.user_private_response_table,
                response.event_id
            )
        ).fetchall()
        if resolve_responses(event_responses):
            notify_cancel(response.event_id)
            cancel_event(response.event_id)

        conn.commit()
