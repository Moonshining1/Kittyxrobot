import asyncio
from datetime import datetime, timedelta
from platform import python_version as pyver
from pyrogram.enums import ChatType
from pyrogram import __version__ as pver
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram import __version__ as lver
from telethon import __version__ as tver
from MukeshRobot.modules.no_sql import add_served_chat, save_id
from MukeshRobot import SUPPORT_CHAT, pbot, BOT_USERNAME, OWNER_ID, BOT_NAME, START_IMG

# Track when the bot starts
START_TIME = datetime.now()

async def member_permissions(chat_id: int, user_id: int):
    perms = []
    member = (await pbot.get_chat_member(chat_id, user_id)).privileges
    if not member:
        return []
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_video_chats:
        perms.append("can_manage_video_chats")
    return perms

PHOTO = [
    "https://envs.sh/STz.jpg",
]

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

# Helper function to calculate uptime
def get_uptime():
    now = datetime.now()
    uptime_sec = (now - START_TIME).total_seconds()
    uptime_str = str(timedelta(seconds=int(uptime_sec)))
    return uptime_str

@pbot.on_message(filters.command("alive"))
async def restart(client, m: Message):
    await m.delete()
    accha = await m.reply("🐳")
    await asyncio.sleep(0.2)
    await accha.edit("🔥")
    await accha.delete()
    await asyncio.sleep(0.3)
    
    umm = await m.reply_sticker(
        "CAACAgUAAxkDAAJHbmLuy2NEfrfh6lZSohacEGrVjd5wAAIOBAACl42QVKnra4sdzC_uKQQ"
    )
    await umm.delete()
    
    owner = await pbot.get_users(OWNER_ID)
    uptime = get_uptime()
    
    await m.reply_photo(
        PHOTO[0],  # Using the first photo in the PHOTO list
        caption=f"""**Hey {m.from_user.first_name},** \n\n 
I am [{BOT_NAME}](t.me/{BOT_USERNAME}) alive and working since {uptime} ✨🥀 \n\n Made by ➛** [🇲σ᭡፝֟ɳ🌙](https://t.me/about_ur_moonshining/5)
        """,
        reply_markup=InlineKeyboardMarkup(Mukesh)
    )

@pbot.on_message(group=1)
async def save_statss(_, m):
    try:
        if m.chat.type == ChatType.PRIVATE:
            save_id(m.from_user.id)
        elif m.chat.type == ChatType.SUPERGROUP:
            add_served_chat(m.chat.id)
        else:
            add_served_chat(m.chat.id)        
    except Exception as e:
        pass
       # await _.send_message(OWNER_ID, f"db error {e}")
