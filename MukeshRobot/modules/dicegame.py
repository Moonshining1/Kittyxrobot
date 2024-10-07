from pyrogram import Client, enums, filters
#from config import *
import asyncio
from MukeshRobot import pbot as mukesh

from pyrogram.handlers import MessageHandler


@mukesh.on_message(filters.command("dsjdjdjnf"))
async def dice(bot, message):
    x=await bot.send_dice(message.chat.id)
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)
  
@mukesh.on_message(filters.command("darndndndt"))
async def dart(bot, message):
    x=await bot.send_dice(message.chat.id, "🎯")
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)

@mukesh.on_message(filters.command("baskjdjdjdet"))
async def basket(bot, message):
    x=await bot.send_dice(message.chat.id, "🏀")
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)
@mukesh.on_message(filters.command("jackpdjdjndot"))
async def basket(bot, message):
    x=await bot.send_dice(message.chat.id, "🎰")
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)
@mukesh.on_message(filters.command("bandndndll"))
async def basket(bot, message):
    x=await bot.send_dice(message.chat.id, "🎳")
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)
@mukesh.on_message(filters.command("footbdjdjfjall"))
async def basket(bot, message):
    x=await bot.send_dice(message.chat.id, "⚽")
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)
__help__ = """
» Available commands for Dice 

● /dice - Dice 🎲
● /dart - Dart 🎯
● /basket - Basket Ball 🏀
● /ball - Bowling Ball 🎳
● /football - Football ⚽
● /jackpot - Spin slot machine 🎰

/⁠ᐠ⁠｡⁠ꞈ⁠｡⁠ᐟ⁠\
"""

__mod_name__ = "Dice"
