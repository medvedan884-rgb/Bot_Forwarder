from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_str = os.getenv("SESSION_STRING")

forum_chat = int(os.getenv("FORUM_CHAT"))  # chat_id твоей форум-группы

with TelegramClient(StringSession(session_str), api_id, api_hash) as client:
    entity = client.get_entity(forum_chat)

    print(f"🔎 Темы форума (chat_id={forum_chat}):\n")
    for msg in client.iter_messages(entity, limit=100):
        if msg.is_topic:
            print(f"📌 Тема: {msg.text} | topic_id: {msg.id}")
