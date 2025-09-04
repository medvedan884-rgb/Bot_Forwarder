from telethon import TelegramClient, events
from flask import Flask
import os
import threading

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
target_chat = int(os.getenv("TARGET_CHAT"))
bot_username = os.getenv("BOT_USERNAME")

client = TelegramClient("user", api_id, api_hash)

@client.on(events.NewMessage(from_users=bot_username))
async def handler(event):
    await event.forward_to(target_chat)

# фейковый веб-сервер (чтобы Render держал сервис живым)
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("✅ Userbot запущен и ждёт сообщения...")
    client.start()
    client.run_until_disconnected()
