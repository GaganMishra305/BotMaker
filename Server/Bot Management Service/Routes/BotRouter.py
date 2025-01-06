from fastapi import APIRouter, Depends, HTTPException
from Controllers.BotController import (
    create_bot_fn,
    get_all_bots_fn,
    get_bot_by_id_fn,
    update_bot_fn,
    delete_bot_fn
)
from Db.get_db import get_db
from Models.BotModel import BotRequestModel

bot_router = APIRouter()

# 1. create
@bot_router.post('/')
async def create_bot(bot: BotRequestModel, db = Depends(get_db)):
    bot = await create_bot_fn(bot, db)
    
    if bot:
        return bot
    else:
        raise HTTPException(403, "Couldn't create bot.")

# 2. read
@bot_router.get('/')
async def get_all_bots(db = Depends(get_db)):
    bots = await get_all_bots_fn(db)
    return bots

@bot_router.get('/{bot_id}')
async def get_bot_by_id(bot_id: str, db = Depends(get_db)):
    bot = await get_bot_by_id_fn(bot_id, db)
    return bot

# 3. update
@bot_router.put('/{bot_id}')
async def update_bot(bot_id: str, bot_update: BotRequestModel, db = Depends(get_db)):
    updated_bot = await update_bot_fn(bot_id, bot_update, db)
    return updated_bot

# 4. delete
@bot_router.delete('/{bot_id}')
async def delete_bot(bot_id: str, db = Depends(get_db)):
    result = await delete_bot_fn(bot_id, db)
    return result