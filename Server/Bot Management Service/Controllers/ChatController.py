from fastapi import HTTPException
from Models.ChatModel import Chat, Message
from typing import List

# 1. Create
async def create_chat_fn(bot_id: str, db):
    chat_collection = db.chats
    
    # Check if bot exists
    bot = db.bots.find_one({'_id': str(bot_id)})
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    chat_dict = {
        'bot_id': str(bot_id),
        'messages': [Message(role = 'system', content = bot['prompt']).to_db()]
    }
    
    result = chat_collection.insert_one(chat_dict)
    if result:
        return result
    raise HTTPException(status_code=400, detail="Failed to create chat")

# 2. Read
async def get_all_chats_fn(db):
    chat_collection = db.chats
    chats = chat_collection.find()
    return list(chats)

async def get_chat_by_id_fn(chat_id: str, db):
    chat_collection = db.chats
    chat = chat_collection.find_one({'_id': str(chat_id)})
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    return chat

async def get_chats_by_bot_id_fn(bot_id: str, db):
    chat_collection = db.chats
    chats = chat_collection.find({'bot_id': str(bot_id)})
    return list(chats)

# 3. Update
async def add_message_to_chat_fn(chat_id: str, message: Message, db):
    chat_collection = db.chats
    chat = chat_collection.find_one({'_id': str(chat_id)})
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    result = chat_collection.update_one(
        {'_id': str(chat_id)},
        {'$push': {'messages': message.to_db()}}
    )

    if result is None:
        raise HTTPException(status_code=400, detail="Could add message")

    return db.chats.find_one({"_id" : chat_id})

async def clear_chat_messages_fn(chat_id: str, db):
    chat_collection = db.chats
    chat = chat_collection.find_one({'_id': str(chat_id)})
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    result = chat_collection.update_one(
        {'_id': str(chat_id)},
        {'$set': {'messages': chat.messages[:1]}}
    )
    
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to clear messages")
    
    return {"message": "Chat messages cleared successfully"}

# 4. Delete
async def delete_chat_fn(chat_id: str, db):
    chat_collection = db.chats
    result = chat_collection.delete_one({'_id': str(chat_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    return {"message": "Chat deleted successfully"}
