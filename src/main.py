import json
import logging

from typing import Annotated, Union
from beanie import init_beanie
from starlette.websockets import WebSocketState
from fastapi import (
    Cookie, 
    Depends, 
    FastAPI, 
    Query, 
    WebSocket, 
    WebSocketException,
    status
    )


from auth.app import router as auth_router
from chat.routers import router as chat_router
from auth.users import current_active_user
from chat.models import Message,Room
from chat.notifier import ConnectionManager
from database import db
from auth.db import User
from chat.controllers import (
    add_user_to_room, 
    get_room, 
    remove_user_from_room, 
    upload_message_to_room,
    get_messages
    )


logger = logging.getLogger(__name__)

app = FastAPI()

manager = ConnectionManager()

async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[Union[str, None], Cookie()] = None,
    token: Annotated[Union[str, None], Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@app.websocket("/ws/{room_name}/{user_name}")
async def websocket_endpoint(websocket: WebSocket, 
                             room_name, user_name,
                             cookie_or_token: Annotated[
                                str, Depends(get_cookie_or_token)
                                ],
                             ):
    try:
        await manager.connect(websocket, room_name)
        # wait for messages
        while True:
            if websocket.application_state == WebSocketState.CONNECTED:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                # add user
                if "type" in message_data and message_data["type"] == "join":
                    await add_user_to_room(user_name, room_name)
                    room = await get_room(room_name)
                    data = {
                        "content": f"{user_name} has entered the chat",
                        "user": {"username": user_name},
                        "room_name": room_name,
                        "type": "entrance",
                        "new_room_obj": room,
                    }
                    await manager.broadcast(
                        f"{json.dumps(data, default=str)}"
                        )
                #getting history
                if "type" in message_data and message_data["type"] == "history":
                    messages = await get_messages(room_name)
                    await manager.broadcast(f"{json.dumps(messages, default=str)}")
                # remove user
                if "type" in message_data and message_data["type"] == "leave":
                    logger.warning(message_data["content"])
                    logger.info("Disconnecting from Websocket")
                    logger.warning("Disconnecting Websocket")
                    await remove_user_from_room(None, 
                                                room_name, 
                                                username=user_name
                                                )
                    room = await get_room(room_name)
                    data = {
                        "content": f"{user_name} has left the chat",
                        "user": {"username": user_name},
                        "room_name": room_name,
                        "type": "dismissal",
                        "new_room_obj": room,
                    }
                    await manager.broadcast(f"{json.dumps(data, default=str)}")
                    await manager.disconnect(websocket, room_name)
                if "type" in message_data and message_data["type"] == "message":
                    await upload_message_to_room(data)
                    logger.info(f"DATA RECIEVED: {data}")
                    await manager.broadcast(f"{data}")
            else:
                logger.warning(
                    f"Websocket state: {websocket.application_state}"
                    ", reconnecting...")
                await manager.connect(websocket, room_name)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logger.error(message)
        # remove user
        logger.warning("Disconnecting Websocket")
        await remove_user_from_room(None, room_name, username=user_name)
        room = await get_room(room_name)
        data = {
            "content": f"{user_name} has left the chat",
            "user": {"username": user_name},
            "room_name": room_name,
            "type": "dismissal",
            "new_room_obj": room,
        }
        # await manager.broadcast(f"{json.dumps(data, default=str)}")
        await manager.disconnect(websocket, room_name)
    

app.include_router(auth_router)
app.include_router(chat_router)

#Connection to DB on start 
@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            User,
            Room,
            Message
        ],
    )

# Checking authentication
@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

