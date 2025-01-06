# Routers/chat_router.py
from fastapi import APIRouter, Depends, HTTPException, Query
from Controllers.ChatController import (
    create_chat_fn,
    get_all_chats_fn,
    get_chat_by_id_fn,
    get_chats_by_bot_id_fn,
    add_message_to_chat_fn,
    clear_chat_messages_fn,
    delete_chat_fn,
    get_chat_history_fn
)
from Db.get_db import get_db
from Models.ChatModel import Chat, Message
from uuid import UUID

chat_router = APIRouter()

# 1. Create new chat
@chat_router.post('/')
async def create_chat(bot_id: str, db = Depends(get_db)):
    return await create_chat_fn(bot_id, db)

# 2. Read operations
@chat_router.get('/')
async def get_all_chats(db = Depends(get_db)):
    return await get_all_chats_fn(db)

@chat_router.get('/{chat_id}')
async def get_chat(chat_id: str, db = Depends(get_db)):
    return await get_chat_by_id_fn(chat_id, db)

@chat_router.get('/bot/{bot_id}')
async def get_chats_by_bot(bot_id: str, db = Depends(get_db)):
    return await get_chats_by_bot_id_fn(bot_id, db)

# 3. Update operations
@chat_router.post('/{chat_id}/messages')
async def add_message(chat_id: str, message: Message, db = Depends(get_db)):
    return await add_message_to_chat_fn(chat_id, message, db)

@chat_router.delete('/{chat_id}/messages')
async def clear_chat_messages(chat_id: str, db = Depends(get_db)):
    return await clear_chat_messages_fn(chat_id, db)

# 4. Delete chat
@chat_router.delete('/{chat_id}')
async def delete_chat(chat_id: str, db = Depends(get_db)):
    return await delete_chat_fn(chat_id, db)

