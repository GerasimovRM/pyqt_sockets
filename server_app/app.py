from fastapi import FastAPI, WebSocket
import uvicorn
import websockets
import asyncio

app = FastAPI()

names = asyncio.Queue()

@app.get("/")
async def root(address):
    await names.put(address)
    return "ok"

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        name = await names.get()
        await websocket.send_text(name)
        data = await websocket.receive_text()



if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000)