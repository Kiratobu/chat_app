from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from auth.db import User
from pydantic import BaseModel, EmailStr, Field


class Message(BaseModel):
    user: User
    content: str = None


class MessageInDB(Message):
    _id: ObjectId
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Room(BaseModel):
    room_name: str
    members: Optional[List[User]] = []
    messages: Optional[List[MessageInDB]] = []
    last_pinged: datetime = Field(default_factory=datetime.utcnow)
    active: bool = False


class RoomInDB(Room):
    _id: ObjectId
    date_created: datetime = Field(default_factory=datetime.utcnow)

