import asyncio
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from MukeshRobot import pbot, SUPPORT_CHAT
from MukeshRobot.modules.sql.afk_sql import set_afk, rm_afk, is_afk
from MukeshRobot.modules.no_sql.afk_db import add_afk, remove_afk

# AFK GIF for default replies
AFK_GIF = "https://giphy.com/gifs/Ql23fmd9qOIseS5r3o"

# Command to set AFK status with an optional reason and media
@pbot.on_message(filters.command("afk"))
async def set_afk_status(client, message: Message):
    user_id = message.from_user.id
    reason = "No reason provided"

    # Check if there is a reason or media
    if len(message.text.split()) > 1:
        reason = message.text.split(maxsplit=1)[1]
    elif message.reply_to_message:
        if message.reply_to_message.photo or message.reply_to_message.sticker:
            reason = "AFK with media!"

    # Set AFK status in both SQL and NoSQL databases
    set_afk(user_id, reason)  # SQL
    await add_afk(user_id, reason)  # NoSQL

    # Respond based on whether the user is AFK with media or just a reason
    if message.reply_to_message and (message.reply_to_message.photo or message.reply_to_message.sticker):
        if message.reply_to_message.photo:
            await message.reply_photo(
                message.reply_to_message.photo.file_id,
                caption=f"**{message.from_user.first_name} is now AFK!**\n\nReason: `{reason}`",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Support", url=f"https://t.me/{SUPPORT_CHAT}")]]
                ),
            )
        elif message.reply_to_message.sticker:
            await message.reply_sticker(
                message.reply_to_message.sticker.file_id,
                caption=f"**{message.from_user.first_name} is now AFK!**\n\nReason: `{reason}`",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Support", url=f"https://t.me/{SUPPORT_CHAT}")]]
                ),
            )
    else:
        # Send a message with GIF confirming AFK status
        await message.reply_animation(
            AFK_GIF,
            caption=f"**{message.from_user.first_name} is now AFK!**\n\nReason: `{reason}`",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Support", url=f"https://t.me/{SUPPORT_CHAT}")]]
            ),
        )

# Command to remove AFK status
@pbot.on_message(filters.command("back"))
async def remove_afk_status(client, message: Message):
    user_id = message.from_user.id

    # Remove AFK status from both SQL and NoSQL databases
    rm_afk(user_id)  # SQL
    await remove_afk(user_id)  # NoSQL

    # Send a message confirming the user is back
    await message.reply(f"**{message.from_user.first_name} is no longer AFK!**")

# Automatically detect AFK users when mentioned or replied to
@pbot.on_message(filters.mentioned | filters.reply)
async def afk_reply(client, message: Message):
    if message.reply_to_message and is_afk(message.reply_to_message.from_user.id):
        user_id = message.reply_to_message.from_user.id
        afk_status, reason = await is_afk(user_id)  # Get AFK reason from NoSQL (MongoDB)

        if afk_status:
            await message.reply(f"**{message.reply_to_message.from_user.first_name}** is currently AFK!\nReason: `{reason}`")

# Handler for automatic AFK detection in group messages
@pbot.on_message(filters.group)
async def group_afk_detection(client, message: Message):
    if is_afk(message.from_user.id):
        user_id = message.from_user.id
        afk_status, reason = await is_afk(user_id)

        if afk_status:
            await message.reply(f"Welcome back, **{message.from_user.first_name}**! You were AFK due to `{reason}`.")
            rm_afk(user_id)
            await remove_afk(user_id)

# Command to check the current AFK users (optional)
@pbot.on_message(filters.command("afkusers"))
async def list_afk_users(client, message: Message):
    afk_users = await get_afk_users()  # Get list of AFK users from NoSQL (MongoDB)
    if afk_users:
        users_list = "\n".join([f"User ID: {user['user_id']}, Reason: {user['reason']}" for user in afk_users])
        await message.reply(f"Currently AFK users:\n{users_list}")
    else:
        await message.reply("No users are currently AFK.")

# Help text for the module
__help__ = """
» Available commands for AFK:

● /afk: This will set you as AFK.
● /afk <reason>: Set AFK with a reason.
● /afk <replied to photo or sticker>: Set AFK with media (photo or sticker).
● /afk <replied to photo or sticker> <reason>: Set AFK with media and a reason.
"""

__mod_name__ = "AFK"

# Start the bot
if __name__ == "__main__":
    pbot.run()
