import sys
sys.path.insert(0, '..')
import json
import logging

from bson import ObjectId

from src.database import db
from src.utils import format_ids
from .models import RoomInDB
from auth.users import get_user
from auth.models import User

logger = logging.getLogger(__name__)

async def insert_room(username,room_name, collection):
    """
    Insert Room to database
    """
    room = {}
    room["room_name"] = room_name
    user = await get_user(username)
    room["members"] = [user] if user is not None else []
    dbroom = RoomInDB(**room)
    response = await collection.insert_one(dbroom.dict())
    res = await collection.find_one({"_id": response.inserted_id})
    res = format_ids(res)
    return res


async def get_room(room_name) -> RoomInDB:
    """
    Get Room from database
    """
    row = await db['Room'].find_one({"room_name": room_name})
    if row is not None:
        row = format_ids(row)
        return row
    else:
        return None

async def get_rooms(filter_list: list = None):
    """
    Get multiple Rooms from database
    """
    if filter_list is None:
        rows = await db['Room'].find().to_list(length=None)
    else:
        rows = await db['Room'].find(
            {"room_name": {"$in": filter_list}}
            ).to_list(length=None)

    row_list = []
    for row in rows:
        f_row = format_ids(row)
        row_list.append(f_row)
    return row_list

async def add_user_to_room(username: str, room_name: str):
    """
    Add User to Room members list
    """
    try:
        room = await get_room(room_name)
        user = await get_user(username)

        username_list = [m["username"] for m in room["members"]]
        if user["username"] not in username_list:
            logger.info(f"Adding {user['username']} to members")
            db['Room'].update_one(
                                  {"_id": ObjectId(room["_id"])}, 
                                  {"$push": {"members": user}}
                                  )
            return True
        else:
            logger.info(f"{user['username']} is already a member")
            return True
    except Exception as e:
        logger.error(f"Error updating members: {e}")
        return None

async def remove_user_from_room(user: User, room_name: str, username=None):
    """
    Remove User from Room members list
    """
    try:
        room = await get_room(room_name)
        if username is not None and user is None:
            user = await get_user(username)
        username_list = [m["username"] for m in room["members"]]
        if user["username"] in username_list:
            logger.info(
                f"Removing {user['username']} from {room_name} members")
            db['Room'].update_one(
                {"_id": ObjectId(room["_id"])}, 
                {"$pull": {"members": {"username": user["username"]}}}
            )
            return True
        else:
            logger.info(f"{user['username']} is already out of the room")
            return True
    except Exception as e:
        logger.error(f"Error updating members: {e}")
        return False
    
async def upload_message_to_room(data):
    """
    Uploading messages to room
    """
    message_data = json.loads(data)
    try:
        room = await get_room(message_data["room_name"])
        user = await get_user(message_data["user"]["username"])
        message_data["user"] = user
        message_data["room"] = room
        collection = db['Message']
        await collection.insert_one(message_data)
        return True
    except Exception as e:
        logger.error(f"Error adding message to DB: {type(e)} {e}")
        return False


async def set_room_activity(room_name, activity_bool):
    room = await get_room(room_name)
    if room is not None:
        _id = room["_id"]
        try:
            result = db['Room'].update_one(
                                           {"_id": ObjectId(_id)}, 
                                           {"$set": {"active": activity_bool}}
                                           )
            logger.info(f"Updated room activity {result}")
        except Exception as e:
            logger.error(f"ERROR SETTING ACTIVITY: {e}")
        new_doc = await get_room(room_name)
        return new_doc
    else:
        return None
    
    
async def get_messages(room_name):
    messages = await db['Message'].find({"room.room_name":room_name}).to_list(length=None)
    row_list = []
    for row in messages:
        f_row = format_ids(row)
        row_list.append(f_row)
    return row_list