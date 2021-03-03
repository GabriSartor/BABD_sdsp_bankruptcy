from fastapi import APIRouter
from typing import Optional

from ..database.database import retrieve_tweets, retrieve_tweet
from ..models.tweet import ResponseModel, ErrorResponseModel

router = APIRouter()

@router.get("/", response_description="tweets retrieved")
async def get_tweets(skip: int = 0, limit: int = 20, keyWord: Optional[str] = None):
    tweets = await retrieve_tweets(skip=skip, limit=limit, search=keyWord)
    return ResponseModel(tweets, "tweets data retrieved successfully") \
        if len(tweets) > 0 \
        else ResponseModel(
        tweets, "Empty list returned")


@router.get("/{id}", response_description="tweet data retrieved")
async def get_tweet_data(id):
    tweet = await retrieve_tweet(id)
    return ResponseModel(tweet, "tweet data retrieved successfully") \
        if tweet \
        else ErrorResponseModel("An error occured.", 404, "tweet doesn'exist.")