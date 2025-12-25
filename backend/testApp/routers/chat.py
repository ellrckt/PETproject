from fastapi import APIRouter, WebSocket


router = APIRouter(prefix="/ws", tags=["ws"])


# ws:room:users:{room_id: [{user_id:websocket,user_id2: websocket}]}


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/{room_id}/{user_id}")
async def personal_chat(websocket: WebSocket, room_id: int, user_id: int):
    await websocket.accept()
    while True:
        data = await websocket.receive()
        message = await websocket.send(f"{user_id}:\n{data}")
        print(websocket)
