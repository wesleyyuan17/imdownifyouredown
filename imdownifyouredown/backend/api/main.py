from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return "Welcome to I'm Down If You're Down"
