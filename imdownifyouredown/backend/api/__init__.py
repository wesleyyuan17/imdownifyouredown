from fastapi import APIRouter

from backend.api import (
    main,
    login,
    event,
    user
)

api_router = APIRouter()
api_router.include_router(main.router, tags=["home"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(event.router, tags=["event"])
api_router.include_router(user.router, tags=["user"])
