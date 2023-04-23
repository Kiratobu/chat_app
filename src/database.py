import motor.motor_asyncio

from config import MONGO_PORT, MONGO_USER, MONGO_PASS

#Connection to databse
DATABASE_URL =f"mongodb://{MONGO_USER}:{MONGO_PASS}@mongodb:{MONGO_PORT}"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["database_name"]

