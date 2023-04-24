import sys

from bson import ObjectId
sys.path.insert(0, '..')

import logging

from src.database import db
from src.utils import format_ids
from .models import RoomInDB

logger = logging.getLogger(__name__)

async def insert_room(room_name, collection):
    room = {}
    room["room_name"] = room_name
    dbroom = RoomInDB(**room)
    response = await collection.insert_one(dbroom.dict())
    res = await collection.find_one({"_id": response.inserted_id})
    res["_id"] = str(res["_id"])
    return res


async def get_room(room_name) -> RoomInDB:
    row = await db['Room'].find_one({"room_name": room_name})
    if row is not None:
        row = format_ids(row)
        return row
    else:
        return None
