import asyncio
from fastapi import FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse('events.html', {'request': request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    feed, _ = await asyncio.open_connection('localhost', 5000)
    while True:
        data = await feed.read(512)
        await websocket.send_text(data.decode())
