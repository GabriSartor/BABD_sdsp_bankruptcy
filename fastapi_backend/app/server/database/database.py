import motor.motor_asyncio
from bson import ObjectId
from decouple import config

from .database_helper import tweets_helper

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.babd_sdps

tweets_collection = database.get_collection('tweets')

async def retrieve_tweets(skip=0, limit=20, search=""):
    tweets = []
    async for tweet in tweets_collection.find({"$text": {"$search": search}}, skip=skip, limit=limit):
        tweets.append(tweets_helper(tweet))
    return tweets

async def retrieve_tweet(id: str) -> dict:
    tweet = await tweets_collection.find_one({"_id": ObjectId(id)})
    if tweet:
        return tweets_helper(tweet)
