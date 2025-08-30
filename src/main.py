from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from src.services.connection import connection_manager


app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")


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
