import asyncio
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from pyrogram.types import Message

from MukeshRobot import BOT_NAME, BOT_USERNAME, SUPPORT_CHAT, pbot

# Store the bot start time
START_TIME = datetime.now()

MISHI = [
    "https://envs.sh/STz.jpg"
]# Use a single image URL

# Create the inline keyboard for the reply messag
Mukesh = [
    [
        InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇ", url="https://t.me/kittyxupdates"),
        InlineKeyboardButton(text="ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
    [
        InlineKeyboardButton(
                text="˹🕸️ ᴛᴧᴘ тᴏ sᴇᴇ ᴍᴧɢɪᴄ 🕸️˼",
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]

# Function to calculate uptime
def get_readable_time():
    now = datetime.now()
    uptime_duration = now - START_TIME
    days = uptime_duration.days
    hours, remainder = divmod(uptime_duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

@pbot.on_message(filters.command("alive"))
async def alive_command(client, m: Message):
    try:
        await m.delete()
        loading_message = await m.reply("🐳")
        await asyncio.sleep(0.2)
        await loading_message.edit("🐋")
        await asyncio.sleep(0.1)
        await loading_message.edit("💤")
        await asyncio.sleep(0.1)
        await loading_message.edit("🎉")

        await loading_message.delete()
        await asyncio.sleep(0.3)

        # Send a fun sticker before showing the alive message
        sticker_message = await m.reply_sticker(
            "CAACAgUAAxkDAAJHbmLuy2NEfrfh6lZSohacEGrVjd5wAAIOBAACl42QVKnra4sdzC_uKQQ"
        )
        await sticker_message.delete()
        await asyncio.sleep(0.2)

        # Get the formatted uptime string
        uptime = get_readable_time()

        # Reply with the alive status message
        await m.reply_photo(
            photo=MISHI,
            caption=(
                f"**Hey {m.from_user.first_name},\n\n"
                f"I am [{BOT_NAME}](t.me/{BOT_USERNAME}) alive and working since {uptime} ✨🥀 \n\n"
                "**Made by ➛** [🇲σ᭡፝֟ɳ🌙](https://t.me/about_ur_moonshining/5)"
            ),
            reply_markup=InlineKeyboardMarkup(Mukesh)
        )
    except Exception as e:
        print(f"Error in /alive command: {e}")
        await m.reply(f"Something went wrong while checking bot status. Error: {str(e)}")

__mod_name__ = "Alive"
__help__ = """
 ❍ /alive ➛ Check bot alive status.
 ❍ /ping ➛ Check ping status.
 ❍ /stats ➛ Shows overall stats of the bot.

☆✧....𝐁𝐘🫧 » [☄️𝐌ᴏᴏɳ🌙](https://t.me/Moonshining2)....🥀🥀✧☆
"""
