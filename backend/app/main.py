from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

from app.api.endpoints import router as api_router

app = FastAPI(title="AI Career Agent API", version="1.0.0")

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Career Agent Backend"}
