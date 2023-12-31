from typing import Any

from imdownifyouredown.backend.crud.util import (
    TABLE_SCHEMAS,
    Event,
    EventResponse,
    get_conn
)
from imdownifyouredown.backend.db.config import config


def _resolve_db_table(ctx):
    pass


def get_event(
    event: Event | int,
    db_name: str | None = None
) -> list:
    db_name = db_name or config.db_name
    if isinstance(event, int):
        event_id = event
    elif isinstance(event, Event):
        event_id = event.event_id
    else:
        raise TypeError(f"Unknown type for event: {type(event)}")
    
    with get_conn(db_name, read_only=True) as conn:
        result = conn.execute(
            "SELECT * FROM {} WHERE eventid = {}".format(
                config.events_table,
                event_id
            )
        ).fetchall()
        assert len(result) == 1
        return dict(zip(TABLE_SCHEMAS[config.events_table], result[0]))


def insert_event(
    event: Event,
    db_name: str | None = None
) -> None:
    db_name = db_name or config.db_name
    with get_conn(db_name) as conn:
        conn.executemany(
            f"INSERT INTO {config.events_table} VALUES (?, ?, ?, ?)",
            [
                (event.event_id, event.event_name, event.users, True)
            ]
        )

        # add event to users, initialize responses
        sql = "SELECT * FROM {} WHERE userid IN {}".format(
            config.user_info_table,
            tuple(event.users)
        )
        user_info = conn.execute(sql).fetchall()
        for ui in user_info:
            userid, username, currentevents, numpastevents = ui
            conn.execute(
                "DELETE FROM {} WHERE userid = {}".format(
                    config.user_info_table,
                    userid
                )
            )
            conn.executemany(
                f"INSERT INTO {config.user_info_table} VALUES (?, ?, ?, ?)",
                [
                    (userid, username, currentevents + [event.event_id], numpastevents + 1)
                ]
            )

        for user in event.users:
            sql = "INSERT INTO {} VALUES ({}, {}, {})".format(
                config.user_public_response_table,
                event.event_id,
                user,
                EventResponse.NoResponse.value
            )
            conn.execute(sql)
            sql = "INSERT INTO {} VALUES ({}, {}, {})".format(
                config.user_private_response_table,
                event.event_id,
                user,
                EventResponse.NoResponse.value
            )
            conn.execute(sql)
        
        conn.commit()


def cancel_event(
    event_id: int,
    db_name: str | None = None
) -> None:
    db_name = db_name or config.db_name
    with get_conn(db_name) as conn:
        users = conn.execute(
            f"SELECT users FROM {config.events_table} WHERE eventid = {event_id}"
        ).fetchall()[0][0]
        # remove event from event/response tables
        for tbl in [
            config.events_table,
            config.user_public_response_table,
            config.user_private_response_table
        ]:
            sql = "DELETE FROM {} WHERE eventid = {}".format(tbl, event_id)
            conn.execute(sql)

        # remove event from current events of users
        sql = "SELECT * FROM {} WHERE userid IN {}".format(
            config.user_info_table,
            tuple(users)
        )
        user_info = conn.execute(sql).fetchall()
        for ui in user_info:
            userid, username, currentevents, numpastevents = ui
            currentevents.remove(event_id)
            conn.execute(
                "DELETE FROM {} WHERE userid = {}".format(
                    config.user_info_table,
                    userid
                )
            )
            conn.executemany(
                f"INSERT INTO {config.user_info_table} VALUES (?, ?, ?, ?)",
                [
                    (userid, username, currentevents, numpastevents - 1)
                ]
            )

        conn.commit()


def edit_event(
    event_id: int,
    new_params: dict[str, Any],
    db_name: str | None = None
) -> None:
    db_name = db_name or config.db_name
    with get_conn(db_name) as conn:
        event_params = dict(
            zip(
                ["event_id", "event_name", "users", "live"],
                conn.execute(
                    "SELECT * FROM {} WHERE eventid = {}".format(
                        config.events_table,
                        event_id
                    )
                ).fetchall()[0]
            )
        )
        event_params.update(new_params)
        new_event = Event(**event_params)

        conn.execute(
            "DELETE FROM {} WHERE eventid = {}".format(
                config.events_table,
                event_id
            )
        )
        conn.executemany(
            f"INSERT INTO {config.events_table} VALUES (?, ?, ?, ?)",
            [
                (new_event.event_id, new_event.event_name, new_event.users, new_event.live)
            ]
        )
        conn.commit()
