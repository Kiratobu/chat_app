from beanie import init_beanie
from database import db
from auth.db import User
from fastapi import Depends, FastAPI
from auth.app import router as auth_router
from chat.routers import router as chat_router
from auth.users import current_active_user
from chat.models import Message,Room

app = FastAPI()


app.include_router(auth_router)
app.include_router(chat_router)

#Connection to DB on start 
@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            User,
            
        ],
    )

# Checking authentication
@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}