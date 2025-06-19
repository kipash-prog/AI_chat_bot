import os
from dotenv import load_dotenv

# Load .env before any other imports
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from fastapi import FastAPI
import uvicorn
from server.src.routes.chat import chat
api = FastAPI()
api.include_router(chat, prefix="")

@api.get("/test")
async def root():
    return {"msg": "API is Online"}

if __name__ == "__main__":
    if os.environ.get("APP_ENV") == "development":
        uvicorn.run("main:api", host="0.0.0.0", port=3500, workers=4, reload=True)