from fastapi import APIRouter, Depends
from typing import Optional
from server.security import validate_request

from server.database.database import retrieve_reddit_comments, retrieve_reddit_comment, retrieve_reddit_daily_aggregated_comments
from server.models.reddit_comment import ResponseModel, ErrorResponseModel

import datetime

router = APIRouter()

@router.get("/", response_description="reddit comments retrieved")
async def get_reddit_comments(authenticated: bool = Depends(validate_request), skip: int = 0, limit: int = 20, keyWord: Optional[str] = None, before: Optional[datetime.date] = None, after: Optional[datetime.date] = None):
    comms = await retrieve_reddit_comments(skip=skip, limit=limit, search=keyWord, before = before, after = after)
    return ResponseModel(comms, "reddit comments data retrieved successfully") \
        if len(comms) > 0 \
        else ResponseModel(
        comms, "Empty list returned")

@router.get("/daily/count")
async def get_daily_aggregated_count(authenticated: bool = Depends(validate_request), skip: int = 0, limit: int = 20, sorting: Optional[str] = None, aggregation: Optional[str] = None, keyWord: Optional[str] = None, before: Optional[datetime.date] = None, after: Optional[datetime.date] = None):
    comms = await retrieve_reddit_daily_aggregated_comments(skip=skip, limit=limit, search=keyWord, before = before, after = after, aggregation = aggregation, sorting = sorting)
    return ResponseModel(comms, "reddit comments aggregated data retrieved successfully") \
        if len(comms) > 0 \
        else ResponseModel(
        comms, "Empty list returned")

@router.get("/{id}", response_description="reddit comment data retrieved")
async def get_tweet_data(id, authenticated: bool = Depends(validate_request)):
    com = await retrieve_reddit_comment(id)
    return ResponseModel(com, "reddit comment data retrieved successfully") \
        if com \
        else ErrorResponseModel("An error occured.", 404, "comment doesn'exist.")