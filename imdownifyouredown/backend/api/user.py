from fastapi import APIRouter
from dataclasses import dataclass, fields

from imdownifyouredown.backend.api.util import Action
from imdownifyouredown.backend.crud.users import (
    get_user,
    insert_new_user
)
from imdownifyouredown.backend.crud.util import User, UserResponse

router = APIRouter()


@dataclass(frozen=True)
class UserAction:
    action: Action
    user: User


@router.get("/users")
def get_user(user_id: int):
    return get_user(user_id)


@router.get("/users/edit")
def edit_user(action: UserAction):
    if action.action == Action.insert:
        insert_new_user(action.user)
    elif action.action == Action.edit:
        raise NotImplemented("Cannot edit user details yet")
    elif action == Action.delete:
        raise NotImplemented("Cannot delete users yet")
    else:
        raise ValueError("Unknown event action: {}".format(action.action))
