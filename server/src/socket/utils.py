# filepath: c:\Users\HP\fullstack-ai-chatbot\server\src\ws_socket\utils.py
from fastapi import WebSocket, Query, HTTPException, status

async def get_token(websocket: WebSocket, token: str = Query(None)):
    if not token:
        print("No token provided!")
        
    return token