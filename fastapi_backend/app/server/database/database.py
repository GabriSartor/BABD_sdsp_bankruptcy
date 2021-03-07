import motor.motor_asyncio
from bson import ObjectId
from decouple import config
from datetime import date
from datetime import datetime
from datetime import timezone
from .database_helper import reddit_submission_helper, reddit_comment_helper

import os
MONGO_DETAILS = os.environ['MONGO_DETAILS']
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.babd_sdps

reddit_submissions_collection = database.get_collection('reddit_submissions')
reddit_comments_collection = database.get_collection('reddit_comments')

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
    red_comm = await reddit_comments_collection.find_one({"_id": ObjectId(id)})
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
    cursor = reddit_submissions_collection.aggregate(agg_pipeline, { "allowDiskUse" : true })
    items = await cursor.to_list(length=500)
    return items
    
async def retrieve_reddit_daily_aggregated_comments(skip=0, limit=20, search:str=None, aggregation:str=None, before: date = None, after: date=None, sorting: str=None):
    agg_pipeline = list()
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
    
    result = list()
    cursor = reddit_comments_collection.aggregate(agg_pipeline, { "allowDiskUse" : true })
    items = await cursor.to_list(length=500)
    return items

async def retrieve_reddit_top_daily_submission(day:date=None, subreddit: str = None):
    agg_pipeline = list()

    if not day:
        day = datetime.today()
    match_layer = {'$match' : {"created_utc" : dict()}}
    match_layer['$match']["created_utc"]["$lte"] = datetime(day.year, day.month, day.day, 23, 59, 59, 999, tzinfo=timezone.utc).timestamp()
    match_layer['$match']["created_utc"]["$gte"] = datetime(day.year, day.month, day.day, 00, 00, 00, 000, tzinfo=timezone.utc).timestamp()

    if subreddit:
        match_layer['$match']["subreddit"] = subreddit

    agg_pipeline.append(match_layer)

    agg_pipeline.append({'$sort': {'score': -1}})
    agg_pipeline.append({'$limit': 1})
    print(agg_pipeline)
    red_sub = reddit_submissions_collection.aggregate(agg_pipeline, { "allowDiskUse" : True })
    items = await red_sub.to_list(1)
    if items:
        return reddit_submission_helper(items[0])
