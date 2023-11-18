from fastapi import APIRouter

router = APIRouter()


@router.get("/events/{event_id}")
def get_event(event_id: int):
    return {"event_id": event_id}
