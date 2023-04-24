from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .controllers import get_room,insert_room

import sys
sys.path.insert(0, '..')

from src.database import db
from src.utils import format_ids

router = APIRouter()


class RoomCreateRequest(BaseModel):
    username: str
    room_name: str

@router.post("/room", tags=["Rooms"])
async def create_room(
    request: RoomCreateRequest,
):
    """
    Create a room
    """
    response = await insert_room('some_str', db['Room'])
    return response



@router.get("/room/{room_name}", tags=["Rooms"])
async def get_single_room(
    room_name#, current_user: User = Depends(get_current_active_user),
):
    """
    Get Room by room name
    """
    room = await get_room(room_name)
    formatted_room = format_ids(room)
    return formatted_room

