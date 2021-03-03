from fastapi import Depends, FastAPI
#from fastapi.security import OAuth2PasswordBearer

#from .auth.jwt_bearer import JWTBearer
from .routes.tweet import router as tweetRouter
#from .routes.admin import router as AdminRouter

app = FastAPI()

#token_listener = JWTBearer()
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to our public API for BABD - Scalable Data Storage and Processing exam. "+
                        "Visit url/docs to see the Documentation and try the API"}


#app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
#app.include_router(StudentRouter, tags=["Students"], prefix="/student", dependencies=[Depends(token_listener)])
app.include_router(tweetRouter, tags=["tweets"], prefix="/tweets")
