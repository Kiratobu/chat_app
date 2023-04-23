from beanie import init_beanie
from database import db
from auth.db import User
from fastapi import FastAPI
from auth.app import router as auth_router

app = FastAPI()


app.include_router(auth_router)

#Connection to DB on start 
@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            User,
        ],
    )