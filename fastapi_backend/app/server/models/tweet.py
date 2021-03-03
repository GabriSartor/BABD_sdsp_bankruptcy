from pydantic import BaseModel, Field
from datetime import datetime

class tweetModel(BaseModel):
    text: str = Field(...)
    user: str = Field(...)
    positivity: int = Field(...)
    date: datetime = Field(...)
    tweetter_id: str = Field(...)

def ResponseModel(data, message):
    return {
        "data": [
            data
        ],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }
