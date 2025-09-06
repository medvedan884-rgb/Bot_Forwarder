from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
import threading, os

# --- Telegram ---
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_username = os.getenv("BOT_USERNAME")   # от кого слушаем
session_str = os.getenv("SESSION_STRING")
forum_chat = int(os.getenv("FORUM_CHAT"))  # общий chat_id форума

# Темы (topic_id) в форуме
TOPIC_PAYMENT = int(os.getenv("TOPIC_PAYMENT"))     # тема "оплатил покупку"
TOPIC_CONFIRM = int(os.getenv("TOPIC_CONFIRM"))     # тема "подтвердил получение товара"
TOPIC_INBOX = int(os.getenv("TOPIC_INBOX"))         # тема "новое сообщение от пользователя"

# Словарь правил
FORWARD_RULES = {
    "оплатил покупку": TOPIC_PAYMENT,
    "подтвердил получение товара": TOPIC_CONFIRM,
    "новое сообщение от пользователя": TOPIC_INBOX
}

client = TelegramClient(StringSession(session_str), api_id, api_hash)

@client.on(events.NewMessage(from_users=bot_username))
async def handler(event):
    text = event.raw_text.lower()
    print(f"📩 Получено сообщение: {text}")

    for phrase, topic_id in FORWARD_RULES.items():
        if phrase in text:
            await client.send_message(
                forum_chat,
                event.raw_text,      # текст сообщения
                reply_to=topic_id    # указываем тему
            )
            print(f"➡️ Переслано в тему {topic_id} (по фразе: {phrase})")
            break

# --- Flask (чтобы Render не засыпал) ---
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is running!"

def run_flask():
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- Run ---
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print(f"✅ Userbot запущен и ждёт сообщения от @{bot_username}...")
    while True:
        try:
            client.start()
            client.run_until_disconnected()
        except Exception as e:
            print(f"⚠️ Ошибка: {e}, перезапуск...")
