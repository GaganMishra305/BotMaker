# Controllers/BotController.py
from fastapi import HTTPException
from Models.BotModel import BotRequestModel
# 1. create
async def create_bot_fn(bot: BotRequestModel, db):
    # 1. Check for creators
    creator = db.users.find_one({'_id': bot.creator_id})
    if creator is None:
        raise HTTPException(status_code=400, detail="User with given creator id does not exist.")
    
    # 2. save the bot
    bot_collection = db.bots
    saved_bot = bot_collection.insert_one(bot.to_db())
    
    return saved_bot

# 2. read
async def get_all_bots_fn(db):
    bot_collection = db.bots
    bots = bot_collection.find()
    return list(bots)

async def get_bot_by_id_fn(bot_id: str, db):
    bot_collection = db.bots
    bot = bot_collection.find_one({'_id': bot_id})
    
    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    return bot

# 3. update
async def update_bot_fn(bot_id: str, bot_update: BotRequestModel, db):
    # 1. Check if bot exists
    bot_collection = db.bots
    existing_bot = bot_collection.find_one({'_id': bot_id})
    
    if existing_bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    # 2. Check if creator exists
    creator = db.users.find_one({'_id': bot_update.creator_id})
    if creator is None:
        raise HTTPException(status_code=400, detail="User with given creator id does not exist.")
    
    # 3. Update bot
    updated_bot = bot_collection.update_one(
        {'_id': bot_id},
        {'$set': bot_update.to_db()}
    )
    
    if updated_bot.modified_count == 0:
        raise HTTPException(status_code=400, detail="Bot update failed")
    
    return bot_collection.find_one({'_id': bot_id})

# 4. delete
async def delete_bot_fn(bot_id: str, db):
    bot_collection = db.bots
    existing_bot = bot_collection.find_one({'_id': bot_id})
    
    if existing_bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    deleted_bot = bot_collection.delete_one({'_id': bot_id})
    
    if deleted_bot.deleted_count == 0:
        raise HTTPException(status_code=400, detail="Bot deletion failed")
    
    return {"message": "Bot deleted successfully"}
