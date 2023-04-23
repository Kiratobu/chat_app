from beanie import Document
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase


#User model from FastApiUsers package
class User(BeanieBaseUser, Document):
    pass


async def get_user_db():
    yield BeanieUserDatabase(User)



