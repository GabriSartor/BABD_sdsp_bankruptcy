from fastapi import APIRouter
from typing import Optional

from ..database.database import retrieve_reddit_submissions, retrieve_reddit_submission, retrieve_reddit_daily_aggregated_submissions
from ..models.reddit_submission import ResponseModel, ErrorResponseModel

import datetime

router = APIRouter()

@router.get("/", response_description="reddit submissions retrieved")
async def get_reddit_submissions(skip: int = 0, limit: int = 20, keyWord: Optional[str] = None, before: Optional[datetime.date] = None, after: Optional[datetime.date] = None):
    subs = await retrieve_reddit_submissions(skip=skip, limit=limit, search=keyWord, before = before, after = after)
    return ResponseModel(subs, "reddit submissions data retrieved successfully") \
        if len(subs) > 0 \
        else ResponseModel(
        subs, "Empty list returned")

@router.get("/daily/count")
async def get_daily_aggregated_count(skip: int = 0, limit: int = 20, sorting: Optional[str] = None, aggregation: Optional[str] = None, keyWord: Optional[str] = None, before: Optional[datetime.date] = None, after: Optional[datetime.date] = None):
    subs = await retrieve_reddit_daily_aggregated_submissions(skip=skip, limit=limit, search=keyWord, before = before, after = after, aggregation = aggregation, sorting = sorting)
    return ResponseModel(subs, "reddit submissions data retrieved successfully") \
        if len(subs) > 0 \
        else ResponseModel(
        subs, "Empty list returned")


@router.get("/{id}", response_description="reddit submission data retrieved")
async def get_tweet_data(id):
    sub = await retrieve_reddit_submission(id)
    return ResponseModel(sub, "reddit submission data retrieved successfully") \
        if sub \
        else ErrorResponseModel("An error occured.", 404, "submission doesn'exist.")