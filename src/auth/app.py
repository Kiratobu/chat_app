from beanie import init_beanie
from fastapi import Depends, FastAPI,APIRouter

from auth.db import User, db
from auth.schemas import UserCreate, UserRead, UserUpdate
from auth.users import auth_backend, current_active_user, fastapi_users

app = FastAPI()

router = APIRouter(
    prefix="/auth/jwt",
    tags=["Auth"]
)

# Endpoints for register, login and logout
router.include_router(
    fastapi_users.get_auth_router(auth_backend)
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

app.include_router(router)

# Checking authentication
@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

#Connection to DB on start 
@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            User,
        ],
    )