from fastapi import WebSocket


class ChatroomConnectionManager:

    def __init__(self):
        self.active_connections: dict = {}

    async def connect(self, websocket: WebSocket, room_id: str, username: str):
        await websocket.accept()

        if room_id not in self.active_connections.keys():
            self.active_connections[room_id] = set()

        self.active_connections[room_id].add(websocket)
        await self.broadcast(f"User {username} has joined this chatroom. Say hello!", room_id)

    def disconnect(self, websocket: WebSocket, room_id: str):
        self.active_connections[room_id].remove(websocket)

    async def broadcast(self, message: str, room_id: str):
        for connection in self.active_connections[room_id]:
            await connection.send_text(message)
