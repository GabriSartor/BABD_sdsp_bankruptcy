from fastapi import APIRouter, Depends
from typing import Optional
from server.security import validate_request

from server.database.database import retrieve_reddit_submissions, retrieve_reddit_submission, retrieve_reddit_daily_aggregated_submissions, retrieve_reddit_top_daily_submission
from server.models.reddit_submission import ResponseModel, ErrorResponseModel
from server.database.db_redis import cache_top_daily_submission, update_cache_top_daily_submission

import datetime

router = APIRouter()

@router.get("/", response_description="reddit submissions retrieved")
async def get_reddit_submissions(authenticated: bool = Depends(validate_request), skip: int = 0, limit: int = 20, keyWord: Optional[str] = None, before: Optional[datetime.date] = None, after: Optional[datetime.date] = None):
    subs = await retrieve_reddit_submissions(skip=skip, limit=limit, search=keyWord, before = before, after = after)
    return ResponseModel(subs, "reddit submissions data retrieved successfully") \
        if len(subs) > 0 \
        else ResponseModel(
        subs, "Empty list returned")

@router.get("/daily/count")
async def get_daily_aggregated_count(authenticated: bool = Depends(validate_request), skip: int = 0, limit: int = 20, sorting: Optional[str] = None, aggregation: Optional[str] = None, keyWord: Optional[str] = None, before: Optional[datetime.date] = None, after: Optional[datetime.date] = None):
    subs = await retrieve_reddit_daily_aggregated_submissions(skip=skip, limit=limit, search=keyWord, before = before, after = after, aggregation = aggregation, sorting = sorting)
    return ResponseModel(subs, "reddit submissions data retrieved successfully") \
        if len(subs) > 0 \
        else ResponseModel(
        subs, "Empty list returned")

@router.get("/daily/top/")
async def get_daily_top_submission(authenticated: bool = Depends(validate_request), day: Optional[datetime.date] = None, subreddit: Optional[str] = None):
    if not day:
        day = datetime.date.today()
    redis_res = cache_top_daily_submission(day, subreddit)
    if redis_res:
        return ResponseModel(redis_res, "reddit top submission data retrieved successfully")
    
    print("Cache not available, going to MongoDB")
    sub = await retrieve_reddit_top_daily_submission(day= day, subreddit = subreddit)
    print("Updating cache (HOPEFULLY)")
    update_cache_top_daily_submission(day=day, subreddit=subreddit, obj = sub)
    return ResponseModel(sub, "reddit submission data retrieved successfully") \
        if sub \
        else ErrorResponseModel("An error occured.", 404, "submission doesn'exist.")

@router.get("/{id}", response_description="reddit submission data retrieved")
async def get_tweet_data(id,authenticated: bool = Depends(validate_request)):
    sub = await retrieve_reddit_submission(id)
    return ResponseModel(sub, "reddit submission data retrieved successfully") \
        if sub \
        else ErrorResponseModel("An error occured.", 404, "submission doesn'exist.")