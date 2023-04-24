from datetime import datetime 
from beanie import Document
from bson import ObjectId
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from pydantic import Field


#User model from FastApiUsers package
class User(BeanieBaseUser, Document):
    username: str

class UserInDB(User):
    _id: ObjectId
    date_created: datetime = Field(default_factory=datetime.utcnow)

async def get_user_db():
    yield BeanieUserDatabase(User)



