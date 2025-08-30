from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        if websocket in self.active_connections:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await self.send_personal_message(message, connection)

    async def broadcast_except(self, message: str, websocket_except: WebSocket):
        for connection in self.active_connections:
            if connection != websocket_except:
                await self.send_personal_message(message, connection)


connection_manager = ConnectionManager()
