from pyrogram import Client, filters
from pyrogram.types import Message
import phonenumbers
from phonenumbers import geocoder, carrier
import os

API_ID = int(os.environ.get("API_ID", 123456))  # Replace with your API_ID
API_HASH = os.environ.get("API_HASH", "your_api_hash")  # Replace with your API_HASH
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")  # Replace with your BOT_TOKEN

bot = Client("number_tracker_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text("👋 Welcome to the 📞 Number Tracker Bot!

Send any phone number in international format (e.g. +919876543210) to get details.")

@bot.on_message(filters.text)
async def track_number(_, message: Message):
    try:
        phone_number = message.text.strip()
        number = phonenumbers.parse(phone_number)
        location = geocoder.description_for_number(number, "en")
        sim_carrier = carrier.name_for_number(number, "en")

        reply = f"📞 **Number**: `{phone_number}`
🌍 **Location**: `{location}`
📡 **Carrier**: `{sim_carrier}`"
        await message.reply_text(reply)
    except Exception as e:
        await message.reply_text("❌ Invalid number or unsupported format. Please use format like +919876543210.")

bot.run()