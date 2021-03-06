import redis
import os
from datetime import date
from datetime import datetime
from datetime import timezone
from .database_helper import reddit_submission_helper, reddit_comment_helper
import json

db = redis.StrictRedis('redis')

def cache_top_daily_submission(day:date=None, subreddit: str = None):
    if not subreddit:
        subreddit = "all"
    key = "reddit_top_submission_{}_{}".format(day.isoformat(), subreddit)
    res = db.execute_command('JSON.GET', key)
    if not res:
        return None
    else:
        return (json.loads(db.execute_command('JSON.GET', key)))


def update_cache_top_daily_submission(day:date=None, subreddit: str = None, obj = None, ex = None):
    if not subreddit:
        subreddit = "all"
    key = "reddit_top_submission_{}_{}".format(day.isoformat(), subreddit)
    if not ex:
        ex = 24*60*60
    print("Saving in cache {} {}".format(key, obj))
    db.execute_command('JSON.SET', key, '.', json.dumps(obj))
    return True