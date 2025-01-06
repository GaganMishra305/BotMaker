from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from Db.get_db import connect_db, disconnect_db, get_db

# 1. Db
@asynccontextmanager
async def lifespan(app: FastAPI):
    # app starts
    connect_db()
    # app is on
    yield
    # app shutdowns
    disconnect_db()
    
# ------------------------------------------------------------------------------

# 2. Main app
app = FastAPI(lifespan=lifespan)

# -------------------------------------------------------------------------------

# 3. Routing
from Routes.UserRouter import user_router
from Routes.BotRouter import bot_router
from Routes.ChatRouter import chat_router

@app.get("/")
async def root(db=Depends(get_db)):
    return {"message": "Welcome to Bot Maker!"}

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(bot_router, prefix="/bot", tags=["Bot"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

if __name__ == "__main__":
    uvicorn.run(app)
