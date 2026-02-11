from flask import Flask, request, jsonify, Response
import requests
import json
import os
import time
import datetime
from html import escape # Equivalent to htmlspecialchars

app = Flask(__name__)

# Environment variable for the Bot Token
BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# --- Helper Functions ---

def telegram_api_call(method, data=None):
    """A helper function to make API calls to Telegram."""
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN is not set.")
        return {"ok": False, "error": "Bot token missing"}

    url = f"{TELEGRAM_API_URL}/{method}"
    
    # Ensure all data parameters are properly encoded for GET/POST request
    # Since we are using a standard POST request with data payload, http_build_query logic is handled by requests library
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Telegram API call failed ({method}): {e}")
        return {"ok": False, "error": str(e)}

def send_message(chat_id, text, keyboard=None, reply_to=None):
    """PHP's sendMessage equivalent in Python."""
    if not chat_id or not text:
        return

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    if keyboard:
        payload["reply_markup"] = json.dumps(keyboard)

    if reply_to:
        payload["reply_to_message_id"] = reply_to
        payload["allow_sending_without_reply"] = True

    return telegram_api_call("sendMessage", payload)

# --- Main Webhook Handler ---

@app.route("/", methods=["POST"])
def telegram_webhook():
    update = request.get_json(silent=True)
    if not update or "message" not in update:
        return jsonify({"status": "ok"})

    message = update.get("message", {})
    
    # Extract common variables
    chat_id = message.get("chat", {}).get("id")
    message_id = message.get("message_id")
    text = message.get("text", "")
    
    # Specific fields for shared messages
    user_shared = message.get("user_shared")
    chat_shared = message.get("chat_shared")

    # --- Command Handlers ---

    if text == "/start":
        welcome = (
            "👋 <b><u>𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 Hyper Smart Chat-ID</u></b>\n"
            "<i>𝐘𝐨𝐮𝐫 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐈𝐃 𝐓𝐨𝐨𝐥𝐤𝐢𝐭</i>\n"
            "━━━━━━━━━━━━━━━\n\n"
            "📌 <b><u>𝗪𝐡𝐚𝐭 𝐈𝐭 𝐃𝐨𝐞𝐬</u></b>\n"
            "🔍 Instantly fetch <b>Telegram IDs</b> of any <i>User</i>, <i>Group</i>, or <i>Channel</i>.\n"
            "📎 Get:\n"
            "   • 🧾 Name or Title\n"
            "   • 🆔 Telegram ID\n\n"
            "👨‍💻 <b><u>𝐈𝐝𝐞𝐚𝐥 𝐅𝐨𝐫</u></b>\n"
            "• Developers & Admins\n"
            "• Identity Checkers\n\n"
            "━━━━━━━━━━━━━━━\n"
            "🚀 <b><u>𝐂𝐫𝐞𝐝𝐢𝐭𝐬</u></b>\n"
            "🔹 Powered by: <a href='https://t.me/Hyper_10_Squad'>𝐇𝐲𝐩𝐞𝐫 𝐒𝐪𝐮𝐚𝐝 🛡️</a>\n"
            "🔧 Developer: <a href='tg://user?id=7870904106'>𝐇𝐂𝟒𝐊 𝐎𝐖𝐍𝐄𝐑 🛡️</a>\n"
            "━━━━━━━━━━━━━━━\n\n"
            "✅ <b><u>𝐒𝐡𝐚𝐫𝐞 & 𝐆𝐞𝐭 𝐈𝐃𝐬 𝐍𝐨𝐰</u></b>"
        )

        keyboard = {
            "keyboard": [
                [
                    {"text": "🧑‍💼 𝗨𝘀𝗲𝗿", "request_user": {"request_id": 1, "user_is_bot": False}}
                ],
                [
                    {"text": "🔐 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹", "request_chat": {"request_id": 2, "chat_is_channel": True, "chat_has_username": False}},
                    {"text": "👤 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗚𝗿𝗼𝘂𝗽", "request_chat": {"request_id": 3, "chat_is_channel": False, "chat_has_username": False}}
                ],
                [
                    {"text": "📣 𝗣𝘂𝗯𝗹𝗶𝗰 𝗖𝗵𝗮𝗻𝗻𝗲𝗹", "request_chat": {"request_id": 4, "chat_is_channel": True, "chat_has_username": True}},
                    {"text": "👨‍👩‍👦 𝗣𝘂𝗯𝗹𝗶𝗰 𝗚𝗿𝗼𝘂𝗽", "request_chat": {"request_id": 5, "chat_is_channel": False, "chat_has_username": True}}
                ],
                [
                    {"text": "🤖 𝗕𝗼𝘁 𝗔𝗰𝗰𝗼𝘂𝗻𝘁", "request_user": {"request_id": 6, "user_is_bot": True}}
                ]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": True
        }
        send_message(chat_id, welcome, keyboard, message_id)

    elif text == "/me":
        from_user = message.get("from")
        if from_user:
            first_name = escape(from_user.get("first_name", "Unknown"))
            last_name = escape(from_user.get("last_name", ""))
            username = "@" + escape(from_user.get("username", "Not set")) if from_user.get("username") else "Not set"
            user_id = from_user.get("id", "Unknown")

            full_name = f"{first_name} {last_name}".strip()

            reply = (
                "👤 <b><u>𝗬𝗼𝘂𝗿 𝗜𝗻𝗳𝗼</u></b>\n"
                f"📛 <b><u>𝗡𝗮𝗺𝗲:</u></b> <code>{full_name}</code>\n"
                f"🔖 <b><u>𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲:</u></b> <code>{username}</code>\n"
                f"🆔 <b><u>𝗨𝘀𝗲𝗿 𝗜𝗗:</u></b> <code>{user_id}</code>"
            )
            send_message(chat_id, reply, None, message_id)
        else:
            send_message(chat_id, "❌ Sorry, could not fetch your information.", None, message_id)

    elif text == "/dev":
        reply = (
            "👨‍💻 <b><u>𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿 𝗜𝗻𝗳𝗼</u></b>\n"
            "━━━━━━━━━━━━━━━\n"
            "🔧 <b>𝗡𝗮𝗺𝗲:</b> <a href='tg://user?id=7870904106'>𝐇𝐂𝟒𝐊 𝐎𝐖𝐍𝐄𝐑 🛡️</a>\n"
            "📢 <b>𝗖𝗵𝗮𝗻𝗻𝗲𝗹:</b> <a href='https://t.me/Hyper_10_Squad'>𝐇𝐲𝐩𝐞𝐫 𝐒𝐪𝐮𝐚𝐝 🔰</a>\n"
            "🌍 <b>𝗖𝗼𝘂𝗻𝘁𝗿𝘆:</b> <a href='https://www.google.com/maps/place/Bangladesh'>🇧🇩 Bangladesh</a>\n"
            "🏙️ <b>𝗗𝗶𝘀𝘁𝗿𝗶𝗰𝘁𝘀:</b>\n"
            " 📍 <a href='https://www.google.com/maps/place/Panchagarh'>Hyper Limited – Panchagarh</a>\n"
            " 📍 <a href='https://www.google.com/maps/place/Rangpur'>Hyper Limited – Rangpur</a>\n"
            "━━━━━━━━━━━━━━━\n\n"
            "💡 <i>Empowering Telegram with smart tools and real-time ID fetchers.</i>\n"
            "🛡️ <b>𝐓𝐞𝐜𝐡 𝐈𝐬 𝐎𝐮𝐫 𝐒𝐡𝐢𝐞𝐥𝐝, 𝐂𝐨𝐝𝐞 𝐈𝐬 𝐎𝐮𝐫 𝐖𝐞𝐚𝐩𝐨𝐧</b>"
        )
        button = {
            "inline_keyboard": [
                [
                    {"text": "🛠️ 𝐉𝐨𝐢𝐧 @𝐇ʏᴘᴇʀ_𝟏𝟎_𝐒ǫᴜᴀᴅ", "url": "https://t.me/Hyper_10_Squad"}
                ]
            ]
        }
        send_message(chat_id, reply, button, message_id)

    elif text == "/info":
        bot_info_res = telegram_api_call("getMe")
        
        bot_name = "Unknown"
        bot_username = "@unknown_bot"

        if bot_info_res["ok"]:
            bot_data = bot_info_res["result"]
            bot_name = escape(bot_data.get("first_name", "Unknown"))
            bot_username = "@" + bot_data.get("username", "unknown_bot")

        created_date = "2024-06-15" # Hardcoded as per PHP script
        last_updated = datetime.date.today().strftime("%Y-%m-%d")

        reply = (
            "ℹ️ <b><u>𝐁𝐨𝐭 𝐈𝐧𝐟𝐨</u></b>\n"
            "━━━━━━━━━━━━━━━\n"
            f"🤖 <b>𝐁𝐨𝐭 𝐍𝐚𝐦𝐞:</b> <b>{bot_name}</b>\n"
            f"🔖 <b>𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞:</b> <b>{bot_username}</b>\n"
            f"📆 <b>𝐂𝐫𝐞𝐚𝐭𝐞𝐝:</b> {created_date}\n"
            f"♻️ <b>𝐋𝐚𝐬𝐭 𝐔𝐩𝐝𝐚𝐭𝐞:</b> {last_updated}\n"
            "👨‍💻 <b>𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫:</b> <a href='tg://user?id=7870904106'>𝐇𝐂𝟒𝐊 𝐎𝐖𝐍𝐄𝐑 🛡️</a>\n"
            "━━━━━━━━━━━━━━━\n\n"
            "✅ <i>Track and manage bot info in real-time</i>"
        )
        button = {
            "inline_keyboard": [
                [
                    {"text": "🛠️ 𝐉𝐨𝐢𝐧 @𝐇ʏᴘᴇʀ_𝟏𝟎_𝐒ǫᴜᴀᴅ", "url": "https://t.me/Hyper_10_Squad"}
                ]
            ]
        }
        send_message(chat_id, reply, button, message_id)

    elif text == "/community":
        reply = (
            "🤖 <b><u>𝐂𝐨𝐦𝐦𝐮𝐧𝐢𝐭𝐲 𝐇𝐮𝐛</u></b>\n"
            "━━━━━━━━━━━━━━━\n"
            "🛠️ <b>𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫:</b> <a href='https://t.me/HC4K_OWNER'>𝐇𝐂𝟒𝐊 𝐎𝐖𝐍𝐄𝐑 🛡️</a>\n"
            "🔗 <b>𝐎𝐟𝐟𝐢𝐜𝐢𝐚𝐥 𝐂𝐡𝐚𝐧𝐧𝐞𝐥:</b> <a href='https://t.me/Hyper_10_Squad'>𝐇𝐲𝐩𝐞𝐫 𝐒𝐪𝐮𝐚𝐝 🛡️</a>\n"
            "━━━━━━━━━━━━━━━\n\n"
            "📢 <b>𝐉𝐨𝐢𝐧 𝐨𝐮𝐫 𝐨𝐟𝐟𝐢𝐜𝐢𝐚𝐥 𝐛𝐨𝐭 𝐜𝐨𝐦𝐦𝐮𝐧𝐢𝐭𝐲</b> to get access to:\n"
            "✅ Smart & advanced bot features\n"
            "🎯 Exclusive updates & new tools\n"
            "🤝 Connect with other bot lovers\n\n"
            "📌 <i>Our mission is to bring powerful bots to your fingertips — join the revolution!</i>"
        )
        button = {
            "inline_keyboard": [
                [
                    {"text": "🛠️ 𝐉𝐨𝐢𝐧 @𝐇ʏᴘᴇʀ_𝟏𝟎_𝐒ǫᴜᴀᴅ", "url": "https://t.me/Hyper_10_Squad"}
                ]
            ]
        }
        send_message(chat_id, reply, button, message_id)

    # --- Shared User/Chat Handlers ---

    if user_shared and "user_id" in user_shared:
        shared_user_id = user_shared["user_id"]
        chat_res = telegram_api_call("getChat", {"chat_id": shared_user_id})
        
        name = "Unknown"
        if chat_res["ok"]:
            user = chat_res["result"]
            name = escape(user.get("first_name", "Unknown"))
        
        reply = (
            "👤 <b><u>𝗨𝐬𝐞𝐫 𝐈𝐧𝐟𝐨</u></b>\n"
            f"📛 <b>𝗡𝗮𝗺𝗲:</b> <code>{name}</code>\n"
            f"🆔 <b>𝗨𝘀𝗲𝗿 𝗜𝗗:</b> <code>{shared_user_id}</code>"
        )
        send_message(chat_id, reply, None, message_id)

    elif chat_shared and "chat_id" in chat_shared:
        shared_chat_id = chat_shared["chat_id"]
        chat_res = telegram_api_call("getChat", {"chat_id": shared_chat_id})
        
        title = "❓ Unknown Channel"
        if chat_res["ok"]:
            chat = chat_res["result"]
            title = escape(chat.get("title", "❓ Unknown Channel"))
        
        reply = (
            "💬 <b><u>𝗖𝗵𝗮𝘁 𝗜𝗻𝗳𝗼</u></b>\n"
            f"📛 <b>𝗧𝗶𝘁𝗹𝗲:</b> <code>{title}</code>\n"
            f"🆔 <b>𝗖𝗵𝗮𝘁 𝗜𝗗:</b> <code>{shared_chat_id}</code>"
        )
        send_message(chat_id, reply, None, message_id)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # Note: Vercel doesn't use the 'if __name__ == "__main__":' block. 
    # This is for local testing only.
    app.run(debug=True)
