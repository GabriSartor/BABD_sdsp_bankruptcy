from fastapi import APIRouter
from typing import Optional

from ..database.database import retrieve_reddit_comments, retrieve_reddit_comment
from ..models.reddit_comment import ResponseModel, ErrorResponseModel

import datetime

router = APIRouter()

@router.get("/", response_description="reddit comments retrieved")
async def get_reddit_comments(skip: int = 0, limit: int = 20, keyWord: Optional[str] = None, before: Optional[datetime.date] = None, after: Optional[datetime.date] = None):
    subs = await retrieve_reddit_comments(skip=skip, limit=limit, search=keyWord, before = before, after = after)
    return ResponseModel(subs, "reddit comments data retrieved successfully") \
        if len(subs) > 0 \
        else ResponseModel(
        subs, "Empty list returned")


@router.get("/{id}", response_description="reddit comment data retrieved")
async def get_tweet_data(id):
    sub = await retrieve_reddit_comment(id)
    return ResponseModel(sub, "reddit comment data retrieved successfully") \
        if sub \
        else ErrorResponseModel("An error occured.", 404, "comment doesn'exist.")