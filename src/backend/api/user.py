from fastapi import APIRouter

router = APIRouter()


@router.get("/user/{user_id}")
def get_event(user_id: int):
    return {"user_id": user_id}
