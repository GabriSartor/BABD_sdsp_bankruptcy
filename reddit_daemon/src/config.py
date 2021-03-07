
class Config:
    URL_SUB = "https://api.pushshift.io/reddit/search/submission"
    URL_COMMENTS =  "https://api.pushshift.io/reddit/search/comment"
    URL_COMMENTS_ID =  "https://api.pushshift.io/reddit/submission/comment_ids"

    SUBMISSION_FIELD_LIST = ["id",
                "all_awardings",
                "author",
                "created_utc",
                "full_link",
                "is_video",
                "is_gallery",
                "media_only",
                "num_comments",
                "num_crossposts",
                "score",
                "subreddit",
                "title",
                "selftext"]
                
    COMMENT_FIELD_LIST = ["author",
                        "body",
                        "created_utc",
                        "distinguished",
                        "id",
                        "score",
                        "link_id",
                        "parent_id",
                        "subreddit" ]

    SUBREDDIT_LIST = ["stocks",
                    "options",
                    "investing",
                    "wallstreetbets",
                    "economics",
                    "economy",
                    "business",
                    "news"] 