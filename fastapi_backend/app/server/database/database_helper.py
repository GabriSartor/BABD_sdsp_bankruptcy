def tweets_helper(tweet) -> dict:
    return {
        "mongo_id": str(tweet['_id']),
        "author": tweet['User'],
        "text": tweet['Text'],
        "positivity": tweet['Positivity_score'],
        "date": tweet['DateTime'],
        "tweet_id": tweet['Twitter_ID']
    }
