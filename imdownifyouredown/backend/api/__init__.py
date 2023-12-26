from fastapi import APIRouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from imdownifyouredown.backend.api import (
    root,
    # login,
    event,
    user
)

api_router = APIRouter()
api_router.include_router(root.router, tags=["home", "root"])
# api_router.include_router(login.router, tags=["login"])
api_router.include_router(event.router, tags=["event"])
api_router.include_router(user.router, tags=["user"])

app = FastAPI()
app.include_router(api_router)

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
