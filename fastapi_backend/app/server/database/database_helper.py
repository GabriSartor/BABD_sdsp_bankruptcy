def reddit_submission_helper(red) -> dict:
    return {
        "mongo_id": str(red['_id']),
        "author": red['author'],
        "created_utc": red['created_utc'],
        "full_link": red['full_link'],
        "reddit_id": red['id'],
        "is_video": red['is_video'],
        "media_only": red['media_only'],
        "num_comments": red['num_comments'],
        "num_crossposts": red['num_crossposts'],
        "score": red['score'],
        "selftext": red['selftext'],
        "subreddit": red['subreddit'],
        "title": red['title']
    }

def reddit_comment_helper(red) -> dict:
    return {
        "mongo_id": str(red['_id']),
        "author": red['author'],
        "created_utc": red['created_utc'],
        "link_id": red['link_id'],
        "reddit_id": red['id'],
        "parent_id": red['parent_id'],
        "score": red['score'],
        "body": red['body'],
        "subreddit": red['subreddit'],
        "distinguished": red['distinguished']
    }


