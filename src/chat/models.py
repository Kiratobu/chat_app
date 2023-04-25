from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from auth.models import User
from pydantic import BaseModel, Field
from beanie import Document


class Message(Document, BaseModel):
    user: User
    content: str = None


class MessageInDB(Message):
    _id: ObjectId
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Room(Document, BaseModel):
    room_name: str
    members: Optional[List[User]] = []
    last_pinged: datetime = Field(default_factory=datetime.utcnow)
    active: bool = False


class RoomInDB(Room):
    _id: ObjectId
    date_created: datetime = Field(default_factory=datetime.utcnow)

