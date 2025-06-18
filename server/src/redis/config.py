import os
from dotenv import load_dotenv

# Load the .env file explicitly from the current directory (server/)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Redis():
    def __init__(self):
        self.REDIS_URL = os.environ['REDIS_URL']
        self.REDIS_PASSWORD = os.environ['REDIS_PASSWORD']
        self.REDIS_USER = os.environ['REDIS_USER']
        # Since your REDIS_URL in .env already has the protocol and user info, you may want to adjust this line
        # If REDIS_URL already contains everything, use it directly:
        self.connection_url = self.REDIS_URL
        # Or if you want to build from parts, adjust accordingly

    async def create_connection(self):
        import redis.asyncio as aioredis
        self.connection = aioredis.from_url(self.connection_url, db=0)
        return self.connection
