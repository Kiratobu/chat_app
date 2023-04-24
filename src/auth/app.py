from fastapi import Depends, APIRouter

from auth.db import User
from auth.schemas import UserCreate, UserRead, UserUpdate
from auth.users import auth_backend, current_active_user, fastapi_users



router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# Endpoints for register, login and logout
router.include_router(
    fastapi_users.get_auth_router(auth_backend)
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)



