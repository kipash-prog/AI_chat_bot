from fastapi import WebSocket, Query

async def get_token(websocket: WebSocket, token: str = Query(None)):
    if not token:
        print("No token provided!")
        return None
    return token
