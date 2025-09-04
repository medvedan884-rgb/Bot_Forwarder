from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
target_chat = int(os.getenv("TARGET_CHAT"))
bot_username = os.getenv("BOT_USERNAME")
session_str = os.getenv("SESSION_STRING")

client = TelegramClient(StringSession(session_str), api_id, api_hash)

@client.on(events.NewMessage(from_users=bot_username))
async def handler(event):
    await event.forward_to(target_chat)

print("✅ Userbot запущен и ждёт сообщения...")
client.start()
client.run_until_disconnected()
