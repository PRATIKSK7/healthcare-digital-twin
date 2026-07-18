import os
from fastapi import Security, HTTPException, Request
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED
from slowapi import Limiter
from slowapi.util import get_remote_address
from dotenv import load_dotenv

# Load env variables
load_dotenv()

API_KEY = os.getenv("API_KEY", "dev_secret_key_123")
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )

# Global Rate Limiter
limiter = Limiter(key_func=get_remote_address)
