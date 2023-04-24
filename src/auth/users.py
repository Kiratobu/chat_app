from typing import Optional
from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin

from auth.db import User, get_user_db, UserInDB

import sys
sys.path.insert(0, '..')
from src.database import db
from src.utils import format_ids
from src.config import SECRET

SECRET = f"{SECRET}"


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

# Authentication logic
bearer_transport = BearerTransport(tokenUrl="auth/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)

async def get_user(name) -> UserInDB:
    users_collection = db['User']
    row = await users_collection.find_one({"username": name})
    if row is not None:
        row = format_ids(row)
        return row
    else:
        return None