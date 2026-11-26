import os
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

app = Flask(__name__, static_folder="static", static_url_path="")


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/send", methods=["POST"])
def send():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()[:100]
    contact = str(data.get("contact", "")).strip()[:100]
    message = str(data.get("message", "")).strip()[:2000]

    if not name or not message:
        return jsonify(ok=False, error="Ism va xabarni to'ldiring."), 400
    if not BOT_TOKEN or not CHAT_ID or "bu_yerga" in BOT_TOKEN:
        return jsonify(ok=False, error="Bot sozlanmagan (.env faylini tekshiring)."), 500

    text = f"Saytdan yangi xabar\n\nIsm: {name}\nAloqa: {contact or '-'}\n\n{message}"
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text},
            timeout=10,
        )
        if r.ok:
            return jsonify(ok=True)
        return jsonify(ok=False, error="Telegram xabarni qabul qilmadi."), 502
    except requests.RequestException:
        return jsonify(ok=False, error="Telegramga ulanib bo'lmadi."), 502


if __name__ == "__main__":
    app.run(debug=True, port=5000)
