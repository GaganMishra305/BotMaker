from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
# 1. Main app
app = FastAPI()

# ------------------------------------------------------------------------------

# 2. Getting db
from Db.get_db import connect_db, get_db
@app.on_event("startup")
def startup():
    connect_db()  # Initialize the database connection

@app.on_event("shutdown")
def shutdown():
    print("Shutting down application. Cleanup if needed.")

# -------------------------------------------------------------------------------

# 3. Routing
from Routes.UserRouter import user_router
from Routes.BotRouter import bot_router

@app.get("/")
async def root(db=Depends(get_db)):
    print(db)
    return {"message": "Welcome to Bot Maker!"}
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(bot_router, prefix="/bot", tags=["Products"])

if __name__ == "__main__":
    uvicorn.run(app)
