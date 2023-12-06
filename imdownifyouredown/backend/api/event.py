from fastapi import APIRouter

from imdownifyouredown.backend.crud.events import get_event

router = APIRouter()


@router.get("/events/{event_id}")
def get_event(event_id: int):
    return get_event(event_id)
