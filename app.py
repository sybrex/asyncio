import asyncio
from fastapi import FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.endpoints import WebSocketEndpoint


class Feed:
    def __init__(self):
        self.connections = []

    async def broadcast(self):
        server, _ = await asyncio.open_connection('localhost', 5000)
        while True:
            message = await server.read(1024)
            connections = []
            while len(self.connections) > 0:
                websocket = self.connections.pop()
                await websocket.send_text(message.decode())
                connections.append(websocket)
            self.connections = connections

    def client_connect(self, websocket):
        self.connections.append(websocket)

    def client_disconnect(self, websocket):
        self.connections.remove(websocket)


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')
feed = Feed()


@app.get('/')
async def get(request: Request):
    return templates.TemplateResponse('events.html', {'request': request})


@app.websocket_route('/ws', name='ws')
class Realtime(WebSocketEndpoint):
    async def on_connect(self, websocket):
        await websocket.accept()
        feed.client_connect(websocket)

    async def on_disconnect(self, _websocket: WebSocket, _close_code: int):
        feed.client_disconnect(_websocket)


@app.on_event('startup')
async def startup():
    asyncio.create_task(feed.broadcast())
