from fastapi import FastAPI, WebSocket, Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocketDisconnect
import uvicorn
import redis
import json

from util.ChatroomConnectionManager import ChatroomConnectionManager

app = FastAPI()
manager = ChatroomConnectionManager()
redis_connection = redis.StrictRedis(host="localhost", port=49153)
rooms = {}

# load static content from static directory, assign nickname of 'static'
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialise Jinja2 Templates
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get_index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.websocket("/ws/{chatroom_id}/{client_id}")
async def chatroom_websocket_endpoint(websocket: WebSocket, chatroom_id: str, client_id: str):
    # Add the client to the room, or create a new room if it doesn't exist
    await manager.connect(websocket, chatroom_id, client_id)

    try:
        while True:
            # Receive the message from the client
            message = await websocket.receive_text()

            # convert Dict -> JSON for storage in Redis
            json_data = json.dumps({"client_id": client_id, "message": message})

            # Store the message in Redis, as JSON, with chatroom_id as the key
            redis_connection.set(chatroom_id, json_data)

            # Broadcast the message for all connected clients in the same chatroom
            await manager.broadcast(f"{client_id}: {message}", chatroom_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket, chatroom_id)
        await manager.broadcast(f"User {client_id} has left the chat", chatroom_id)


@app.on_event("shutdown")
async def shutdown_event_handler():
    redis_connection.close()


uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
