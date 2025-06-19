from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from server.src.schema.chat import Chat
from server.src.redis.config import Redis

chat = APIRouter()
redis = Redis()  # Ensure Redis is instantiated properly here


# token route
@chat.post("/token")
async def token_generator(name: str):
    if not name:
        raise HTTPException(status_code=400, detail={"loc": "name", "msg": "Enter a valid name"})

    token = str(uuid.uuid4())
    chat_session = Chat(token=token, messages=[], name=name)

    redis_client = Redis()
    await redis_client.save_json(token, chat_session.dict(), expire_seconds=3600)

    return chat_session.dict()


@chat.websocket("/chat")
async def websocket_chat(websocket: WebSocket, token: str = Query(None)):
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    session = await redis.get_json(token)
    if not session:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
