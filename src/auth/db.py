from config import MONGO_PORT, MONGO_USER, MONGO_PASS
import motor.motor_asyncio
from beanie import Document
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase

#Connection to databse
DATABASE_URL =f"mongodb://{MONGO_USER}:{MONGO_PASS}@mongodb:{MONGO_PORT}"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["database_name"]

#User model from FastApiUsers package
class User(BeanieBaseUser, Document):
    pass


async def get_user_db():
    yield BeanieUserDatabase(User)



