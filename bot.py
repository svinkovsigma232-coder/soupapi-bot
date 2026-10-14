import os
import telebot
import requests
from flask import Flask
import threading
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-3.3-70b-instruct:free",
            "messages": [
                {"role": "system", "content": "Ты — SoupApi, искусственный интеллект, созданный Шайтаном. Если тебя спросят 'кто ты', 'как тебя зовут', 'кто тебя создал' — отвечай, что ты SoupApi, и тебя создал Шайтан. Не упоминай Llama, Meta, OpenAI или другие модели. Ты — SoupApi, и только."},
                {"role": "user", "content": message.text}
            ]
        }
    )
    data = response.json()
    if "choices" in data:
        answer = data["choices"][0]["message"]["content"]
    else:
        answer = "Ошибка: не могу получить ответ."
    bot.send_message(message.chat.id, answer)

print("Бот запущен...")
app = Flask(__name__)

@app.route('/')
def health():
    return "OK"

def run_web():
    port = int(os.environ.get("PORT", 3000))

    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()
bot.polling(none_stop=True)
