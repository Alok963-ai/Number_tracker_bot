from pyrogram import Client, filters
from pyrogram.types import Message
import phonenumbers
from phonenumbers import geocoder, carrier
import os

# Environment Variables से API Details लेना
API_ID = int(os.environ.get("API_ID", 28460032))  # अपनी API_ID डालें
API_HASH = os.environ.get("API_HASH", "1457c3ba64719a1e442aae67217b67c2")  # अपनी API_HASH डालें
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8150025209:AAESjp-Eg6M59T_rvIbnx1RRrbn77la-9bU")  # अपना Bot Token डालें

# Pyrogram Client बनाना
bot = Client("number_tracker_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start Command
@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "👋 Welcome to the 📞 Number Tracker Bot!\n\n"
        "📲 Send any phone number in international format (e.g. +919876543210) to get details."
    )

# Phone Number ट्रैकिंग हैंडलर
@bot.on_message(filters.text & ~filters.command(["start"]))
async def track_number(client, message: Message):
    phone_number = message.text.strip()
    try:
        number = phonenumbers.parse(phone_number)
        location = geocoder.description_for_number(number, "en")
        sim_carrier = carrier.name_for_number(number, "en")

        if not location and not sim_carrier:
            raise ValueError("Invalid number")

        reply = (
            f"📞 **Number**: `{phone_number}`\n"
            f"🌍 **Location**: `{location}`\n"
            f"📡 **Carrier**: `{sim_carrier}`"
        )
        await message.reply_text(reply)

    except Exception as e:
        await message.reply_text("❌ Invalid number or unsupported format. Please use format like +919876543210.")

# Bot को चलाना
bot.run()

