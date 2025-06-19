import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, Query, status
from server.src.schema.chat import Chat
from server.src.redis.config import Redis
from server.src.socket.connection import ConnectionManager
from server.src.socket.utils import get_token   # leaves logging / query‑param parsing to util

chat = APIRouter()
redis = Redis()
manager = ConnectionManager()

# ─────────────────────────── TOKEN ENDPOINT ────────────────────────────
@chat.post("/token")
async def token_generator(name: str):
    if not name.strip():
        raise HTTPException(status_code=400, detail="Enter a valid name")

    token = str(uuid.uuid4())
    session = Chat(token=token, name=name, messages=[])

    # save session JSON (1‑hour TTL)
    await redis.save_json(token, session.dict(), ex=3600)
    return session

# ────────────────────────── WEBSOCKET ENDPOINT ──────────────────────────
@chat.websocket("/chat")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(None)       # pull ?token=… directly
):
    # 1. quick reject if no token
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # 2. check token exists in Redis
    session = await redis.get_json(token)
    if not session:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # 3. accept connection once
    await websocket.accept()
    await manager.connect(websocket)

    # 4. main receive / send loop
    try:
        while True:
            incoming = await websocket.receive_text()
            print(f"[{token}] {incoming}")

            # push into Redis Stream (example)
            conn = await redis.create_connection()
            await conn.xadd("message_channel", {"token": token, "msg": incoming})

            # echo / simulate GPT
            await websocket.send_text("Response: Simulated GPT reply")

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        print("Client disconnected")
