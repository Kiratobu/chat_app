from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .controllers import (
                          get_room, 
                          insert_room,
                          add_user_to_room, 
                          get_rooms,
                          )
from auth.models import User
from auth.users import current_active_user


from src.database import db
from src.utils import format_ids

router = APIRouter()


class RoomCreateRequest(BaseModel):
    username: str
    room_name: str

#Room endpoints
@router.post("/room", tags=["Rooms"])
async def create_room(
    request: RoomCreateRequest,
    current_user: User = Depends(current_active_user),
):
    """
    Create a room
    """
    response = await insert_room(request.username, 
                                 request.room_name, db['Room'])
    return response


@router.get("/room/{room_name}", tags=["Rooms"])
async def get_single_room(
    room_name, current_user: User = Depends(current_active_user),
):
    """
    Get Room by room name
    """
    room = await get_room(room_name)
    formatted_room = format_ids(room)
    return formatted_room

@router.put("/room/{room_name}", tags=["Rooms"])
async def add_user_to_room_members(
    room_name: str, current_user: User = Depends(current_active_user),
):
    """
    Add a user to the room's members
    """
    row = await add_user_to_room(current_user.username, room_name)
    return row

@router.get("/rooms", tags=["Rooms"])
async def get_all_rooms(
    #, current_user: User = Depends(get_current_active_user)
):
    """
    Fetch all available rooms
    """
    rooms = await get_rooms()
    return rooms

