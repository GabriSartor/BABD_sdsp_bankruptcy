import motor.motor_asyncio
from bson import ObjectId
from decouple import config
from datetime import date
from datetime import datetime
from datetime import timezone
from .database_helper import tweets_helper, reddit_submission_helper, reddit_comment_helper

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.babd_sdps

tweets_collection = database.get_collection('tweets')
reddit_submissions_collection = database.get_collection('reddit_submissions')
reddit_comments_collection = database.get_collection('reddit_comments')

async def retrieve_tweets(skip=0, limit=20, search=""):
    tweets = []
    async for tweet in tweets_collection.find({"$text": {"$search": search}}, skip=skip, limit=limit):
        tweets.append(tweets_helper(tweet))
    return tweets

async def retrieve_tweet(id: str) -> dict:
    tweet = await tweets_collection.find_one({"_id": ObjectId(id)})
    if tweet:
        return tweets_helper(tweet)

async def retrieve_reddit_submissions(skip=0, limit=20, search=None, before: date = None, after: date=None):
    query = dict()
    print(before)
    print(after)
    if after or before:
        query["$and"] = list()
    if before:
        query["$and"].append({"created_utc" : { "$lte": datetime(before.year, before.month, before.day, 23, 59, 59, 999, tzinfo=timezone.utc).timestamp() } })
    if after:
        query["$and"].append({"created_utc" : { "$gte": datetime(after.year, after.month, after.day, 00, 00, 00, 000, tzinfo=timezone.utc).timestamp() } })


    if search:
        query["$text"] = {"$search": search}
    
    print(query)
    red_subs = []
    async for red_sub in reddit_submissions_collection.find(query, skip=skip, limit=limit):
        red_subs.append(reddit_submission_helper(red_sub))
    return red_subs

async def retrieve_reddit_comments(skip=0, limit=20, search=None, before: date = None, after: date=None):
    query = dict()
    
    print(before)
    print(after)
    if after or before:
        query["$and"] = list()
    if before:
        query["$and"].append({"created_utc" : { "$lte": datetime(before.year, before.month, before.day, 23, 59, 59, 999, tzinfo=timezone.utc).timestamp() } })
    if after:
        query["$and"].append({"created_utc" : { "$gte": datetime(after.year, after.month, after.day, 00, 00, 00, 000, tzinfo=timezone.utc).timestamp() } })



    if search:
        query["$text"] = {"$search": search}
    
    red_comms = []
    async for red_sub in reddit_comments_collection.find(query, skip=skip, limit=limit):
        red_comms.append(reddit_comment_helper(red_sub))
    return red_comms

async def retrieve_reddit_submission(id: str) -> dict:
    red_sub = await reddit_submissions_collection.find_one({"_id": ObjectId(id)})
    if red_sub:
        return reddit_submission_helper(red_sub)

async def retrieve_reddit_comment(id: str) -> dict:
    red_comm = await reddit_submissions_collection.find_one({"_id": ObjectId(id)})
    if red_comm:
        return reddit_comment_helper(red_comm)
        
async def retrieve_reddit_daily_aggregated_submissions(skip=0, limit=20, search:str=None, aggregation:str=None, before: date = None, after: date=None, sorting: str=None):
    agg_pipeline = list()
    print(before)
    print(after)
    match_layer = {'$match' : dict()}
    if search:
        match_layer['$match']['$text'] = { '$search': search}
    if before or after:
        match_layer['$match']["created_utc"] = dict()
    if before:
        match_layer['$match']["created_utc"]["$lte"] = datetime(before.year, before.month, before.day, 23, 59, 59, 999, tzinfo=timezone.utc).timestamp()
    if after:
        match_layer['$match']["created_utc"]["$gte"] = datetime(after.year, after.month, after.day, 00, 00, 00, 000, tzinfo=timezone.utc).timestamp()

    agg_pipeline.append(match_layer)

    agg_pipeline.append({'$project': {'id': '$id', 
                                    'score': '$score', 
                                    'subreddit': '$subreddit', 
                                    'yearMonthDay': {'$dateToString': {'format': '%Y-%m-%d', 'date': {'$toDate': {'$multiply': ['$created_utc', 1000]}}}}}
                        })
    if sorting:
        sort_list = sorting.split(',')
        sorting_filter = {'$sort': dict() }
        for key in sort_list:
            sorting_filter['$sort'][key] = -1
        agg_pipeline.append(sorting_filter)

    group = {'$group' : { '_id' : { 'day': '$yearMonthDay' }, 
                            'count': {
                                '$sum': 1
                            }, 
                            'best_score': {
                                '$first': '$score'
                            }, 
                            'best_id': {
                                '$first': '$id'
                            }
                        }
            }
    if aggregation:
        aggregation_list = aggregation.split(',')
        for key in aggregation_list:
            group['$group']['_id'][key] = '${}'.format(key)

    agg_pipeline.append(group)

    agg_pipeline.append({'$sort': {'best_score': -1} } )
    
    print(agg_pipeline)
    result = list()
    cursor = reddit_submissions_collection.aggregate(agg_pipeline)
    items = await cursor.to_list(length=500)
    return items
    
        