from fastapi import Header, HTTPException
import os

API_TOKEN = os.getenv("API_TOKEN", "secret123")

def verify_token(x_api_token: str = Header(...)):
    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")
