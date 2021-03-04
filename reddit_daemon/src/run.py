import datetime
import os
#MONGO DB CREDENTIALS

MONGO_PYTHON_DAEMON_USERNAME = os.environ['MONGO_PYTHON_DAEMON_USERNAME']
MONGO_PYTHON_DAEMON_PASSWORD = os.environ['MONGO_PYTHON_DAEMON_PASSWORD']
MONGO_INITDB_DATABASE = os.environ['MONGO_INITDB_DATABASE']

DEV_MODE = os.environ['DEV_MODE']

from pymongo import MongoClient
from database import get_submissions, get_comments_id, get_comments
from config import Config

starting_time = datetime.datetime.now() - datetime.timedelta(24,0)
ending_time = datetime.datetime.now()

client = MongoClient('mongo',
                    username=MONGO_PYTHON_DAEMON_USERNAME,
                    password=MONGO_PYTHON_DAEMON_PASSWORD,
                    authSource=MONGO_INITDB_DATABASE,
                    authMechanism='SCRAM-SHA-1')

db = client[MONGO_INITDB_DATABASE]
sub_coll = db['reddit_submissions']
comm_coll = db['reddit_comments']
sub_coll.delete_many({})
comm_coll.delete_many({})

print("Fetching data from {} to {}".format(starting_time.isoformat(), ending_time.isoformat()))
r_sub = get_submissions(Config.URL_SUB, field_list = Config.SUBMISSION_FIELD_LIST, 
                                    subreddit_list = Config.SUBREDDIT_LIST, 
                                    after = int(starting_time.timestamp()), 
                                    before = int(ending_time.timestamp()))
print("Fetched {} reddit submissions".format(len(r_sub.json()['data'])))
if r_sub.json()['data']:
    sub_coll.insert_many(r_sub.json()['data'])
    for sub in r_sub.json()['data']:
        #Get list of comments
        r_ids = get_comments_id(Config.URL_COMMENTS_ID, r_sub.json()['data'][0]['id'] )
        id_list = r_ids.json()['data']
        if id_list:
            r_comments = get_comments(Config.URL_COMMENTS, field_list = Config.COMMENT_FIELD_LIST, id_list = id_list)
            comm_coll.insert_many(r_comments.json()['data'])

