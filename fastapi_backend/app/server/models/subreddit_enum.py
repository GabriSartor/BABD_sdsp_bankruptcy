from enum import Enum

class SubredditName(str, Enum):
    stocks = "stocks",
    options = "options",
    investing = "investing",
    wallstreetbets = "wallstreetbets",
    economics = "economics",
    economy = "economy",
    business = "business",
    news = "news"

class AggregationFields(str, Enum):
    subreddit = "subreddit",
    author = "author",

class CommentSortingFields(str, Enum):
    score = "score",

class SubmissionSortingFields(str, Enum):
    score = "score",
    num_comments = "num_comments",
    num_crossposts = "num_crossposts"