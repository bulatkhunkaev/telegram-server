from flask import Flask, request, jsonify
from flask_cors import CORS
from aiogram import Bot
import asyncio
import os

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL = "@superbrandchannel"

@app.route("/promo", methods=["POST"])
def promo():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        print("🔍 Получен user_id:", user_id)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        bot = Bot(token=BOT_TOKEN)
        member = loop.run_until_complete(bot.get_chat_member(chat_id=CHANNEL, user_id=user_id))
        loop.run_until_complete(bot.session.close())

        if member.status in ["member", "administrator", "creator"]:
            return jsonify({"promo_code": "WELCOME2025"})
        else:
            return jsonify({"promo_code": "❗ Подпишитесь на канал, чтобы получить промокод."})

    except Exception as e:
        print("❌ Ошибка в сервере:", e)
        return jsonify({"promo_code": "⚠️ Ошибка на сервере. Попробуйте позже."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

