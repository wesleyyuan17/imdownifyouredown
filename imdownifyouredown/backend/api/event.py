from fastapi import APIRouter
from dataclasses import dataclass, fields

from imdownifyouredown.backend.api.util import Action
from imdownifyouredown.backend.crud.events import (
    get_event,
    insert_event,
    edit_event,
    cancel_event
)
from imdownifyouredown.backend.crud.users import (
    record_user_public_response,
    record_user_private_response
)
from imdownifyouredown.backend.crud.util import Event, UserResponse

router = APIRouter()


@dataclass(frozen=True)
class EventAction:
    action: Action
    event: Event


@router.get("/events/{event_id}")
def get_event_info(event_id: int):
    return get_event(event_id)


@router.get("/events/edit/")
def edit_event(action: EventAction):
    if action.action == Action.insert:
        insert_event(action.event)
    elif action.action == Action.edit:
        edit_event(
            action.event.event_id,
            {f.name: getattr(action.event, f) for f in fields(action.event)}
        )
    elif action == Action.delete:
        cancel_event(action.event)
    else:
        raise ValueError("Unknown event action: {}".format(action.action))
    

@router.get("/events/public/")
def new_user_response(event_id: int, response: UserResponse):
    record_user_public_response(response)


@router.get("/events/private/")
def new_user_response(event_id: int, response: UserResponse):
    record_user_private_response(response)
