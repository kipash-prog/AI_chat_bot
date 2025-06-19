import os
import json
import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

class Redis:
    def __init__(self):
        self.connection_url = os.getenv("REDIS_URL")

    async def create_connection(self):
        return redis.from_url(self.connection_url, decode_responses=True)

# redis/config.py

    async def save_json(self, key: str, data: dict, ex: int = 3600):
        conn = await self.create_connection()
        await conn.set(key, json.dumps(data), ex=ex)  # use ex here

    async def get_json(self, key: str):
        conn = await self.create_connection()
        value = await conn.get(key)
        if value:
            return json.loads(value)
        return None
