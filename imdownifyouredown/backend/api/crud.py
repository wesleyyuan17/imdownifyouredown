from fastapi import APIRouter

from dataclasses import dataclass
from enum import Enum

from imdownifyouredown.backend.crud.events import insert_event, cancel_event
from imdownifyouredown.backend.crud.util import Event

router = APIRouter()


class Action(Enum):
    insert = 0
    edit = 1
    delete = 2


@dataclass(frozen=True)
class EventAction:
    action: Action
    event: Event


@router.get("/edit/")
def edit_event(action: EventAction):
    if action.action == Action.insert:
        insert_event(action.event)
    elif action.action == Action.edit:
        pass
    elif action == Action.delete:
        cancel_event(action.event)
    else:
        raise ValueError("Unknown event action: {}".format(action.action))
