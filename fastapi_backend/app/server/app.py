from fastapi import Depends, FastAPI

from .routes.reddit_submission import router as redditSubmissionRouter
from .routes.reddit_comment import router as redditCommentsRouter

tags_metadata = [
    {
        "name": "reddit submissions",
        "description": "Fetch information and data related to reddit submissions. Please **authorize** before using them.",
    },
    {
        "name": "reddit comments",
        "description": "Have fun with 6M reddit comments fetched and stored directly from the Social Network",
    },
]

app = FastAPI(
    title="BABD - Scalable Data Storage and Processing",
    description="This is the public API created by Group 10 for SDSP Project Exam",
    version="0.9",
    openapi_tags=tags_metadata
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to our public API for BABD - Scalable Data Storage and Processing exam."+
                        "Visit _/docs_ to see the Documentation and try the API"}


app.include_router(redditSubmissionRouter, tags=["reddit submissions"], prefix="/reddit/submissions")
app.include_router(redditCommentsRouter, tags=["reddit comments"], prefix="/reddit/comments" )