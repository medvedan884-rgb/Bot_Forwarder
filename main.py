from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
import threading, os

# --- Telegram ---
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_username = os.getenv("BOT_USERNAME")
session_str = os.getenv("SESSION_STRING")

# Чаты для пересылки
CHAT_PAYMENT = int(os.getenv("CHAT_PAYMENT"))       # для "оплатил покупку"
CHAT_CONFIRM = int(os.getenv("CHAT_CONFIRM"))       # для "подтвердил получение товара"
CHAT_INBOX = int(os.getenv("CHAT_INBOX"))           # для "новое сообщение от пользователя"

# Словарь правил (ключ — фраза, значение — чат)
FORWARD_RULES = {
    "оплатил покупку": CHAT_PAYMENT,
    "подтвердил получение товара": CHAT_CONFIRM,
    "новое сообщение от пользователя": CHAT_INBOX
}

client = TelegramClient(StringSession(session_str), api_id, api_hash)

@client.on(events.NewMessage(from_users=bot_username))
async def handler(event):
    text = event.raw_text.lower()
    print(f"📩 Получено сообщение: {text}")

    for phrase, chat_id in FORWARD_RULES.items():
        if phrase in text:
            await event.forward_to(chat_id)
            print(f"➡️ Переслано в чат {chat_id} (по фразе: {phrase})")
            break   # чтобы не сработало несколько раз

# --- Flask ---
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is running!"

def run_flask():
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- Run everything ---
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("✅ Userbot запущен и ждёт сообщения...")
    while True:
        try:
            client.start()
            client.run_until_disconnected()
        except Exception as e:
            print(f"⚠️ Ошибка: {e}, перезапуск...")
