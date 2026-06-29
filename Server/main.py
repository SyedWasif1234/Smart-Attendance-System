from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv

from utils.db import connect_db, disconnect_db

load_dotenv()

# 2. Define the lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs when the server starts
    await connect_db()
    yield
    # This runs when the server shuts down
    await disconnect_db()


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
