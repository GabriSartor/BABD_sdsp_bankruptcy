import secrets
from typing import Optional

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from server.config import API_KEY

api_key = APIKeyHeader(name="token", auto_error=False)

def validate_request(header: Optional[str] = Security(api_key)) -> bool:
    if header is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="No API key provided.", headers={}
        )
    if not secrets.compare_digest(header, str(API_KEY)):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Authentication required.", headers={}
        )
    return True