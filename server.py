from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

clients = []


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


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: int
) -> None:
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.broadcast_except(f"Client #{client_id} says: {data}", websocket)
            await connection_manager.send_personal_message(f"You says: {data}", websocket)
    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket)
        await connection_manager.broadcast(f"Client #{client_id} disconnect")


@app.get("/")
async def get(
    request: Request
) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})
