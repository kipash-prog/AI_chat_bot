from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from fastapi.responses import JSONResponse

from ..redis.producer import Producer
from ..redis.config import Redis
from server.src.socket.utils import get_token
from server.src.socket.connection import ConnectionManager

chat = APIRouter()
manager = ConnectionManager()
redis = Redis()

@chat.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(get_token)):
    # Check if token is provided
    if not token:
        # Close connection with policy violation code
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # Accept the websocket connection here exactly once
    await websocket.accept()

    # Create Redis connection and producer
    redis_client = await redis.create_connection()
    producer = Producer(redis_client)

    # Connect websocket in your connection manager
    await manager.connect(websocket)

    try:
        while True:
            # Receive text message from client
            data = await websocket.receive_text()
            print(f"Received from client: {data}")

            # Prepare stream data with token as key
            stream_data = {token: data}

            # Add message to Redis stream
            message_id = await producer.add_to_stream(stream_data, "message_channel")
            print(f"Message id {message_id} added to message_channel stream")

            # Send a personal response to client (simulate GPT response)
            await manager.send_personal_message(f"Response: Simulating response from the GPT service", websocket)

    except WebSocketDisconnect:
        # Handle websocket disconnection cleanly
        manager.disconnect(websocket)
        print("Client disconnected")
