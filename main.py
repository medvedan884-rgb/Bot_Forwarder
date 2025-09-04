from telethon import TelegramClient, events
import os

# данные из переменных окружения
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
target_chat = int(os.getenv("TARGET_CHAT"))
bot_username = os.getenv("BOT_USERNAME")

client = TelegramClient("user", api_id, api_hash)

@client.on(events.NewMessage(from_users=bot_username))
async def handler(event):
    await event.forward_to(target_chat)

print("✅ Userbot запущен и ждёт сообщения...")
client.start()
client.run_until_disconnected()
