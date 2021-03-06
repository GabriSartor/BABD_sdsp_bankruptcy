client = MongoClient('mongodb://gabriele_sartor:EyQ6YVLZYAcdwkmC@localhost:27017/?authSource=babd_sdps&readPreference=primary&appname=MongoDB%20Compass&ssl=false')
filter={
    '$text': {
        '$search': 'keywords in a list'
    }, 
    'created_utc': {
        '$gte': 21312412, 
        '$lte': 412412412
    }
}

result = client['babd_sdps']['reddit_submissions'].find(
  filter=filter
)