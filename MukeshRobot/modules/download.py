import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
)
from MukeshRobot import (
    BOT_NAME,
    BOT_USERNAME,
    START_IMG,
    SUPPORT_CHAT,
    dispatcher,
    pbot,
)
import MukeshRobot.modules.no_sql.users_db as sql
from MukeshRobot.modules.helper_funcs.chat_status import is_user_admin
from MukeshRobot.modules.helper_funcs.misc import paginate_modules

# --- Available Commands ---
# YouTube: PM-only download handler
def youtube_download(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    message = update.message.text

    # Example: checking for the link and informing user to wait
    if 'youtube.com' in message or 'youtu.be' in message:
        update.message.reply_text(f"Processing your request... Please wait for the download, {update.effective_user.first_name}!")
        # Here would be the logic for downloading the video and sending it back
    else:
        update.message.reply_text("Please send a valid YouTube link.")

# Pinterest: send the link and wait for the download
def pinterest_download(update: Update, context: CallbackContext):
    message = update.message.text

    if 'pinterest.com' in message:
        update.message.reply_text("Processing Pinterest link, please wait...")
        # Logic for downloading and sending Pinterest content
    else:
        update.message.reply_text("Please send a valid Pinterest link.")

# Social Downloader: Twitter, Facebook handler
def social_downloader(update: Update, context: CallbackContext):
    message = context.args[0] if context.args else None
    if message and re.match(r'https?://(www\.)?(twitter|facebook)\.com/', message):
        update.message.reply_text("Processing your request... Please wait!")
        # Logic for downloading content from Twitter or Facebook
    else:
        update.message.reply_text("Please send a valid Twitter/Facebook link in the format /sdl <link>.")

# /start command handler to greet users
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    update.message.reply_text(f"Hello {update.effective_user.first_name}, I am {BOT_NAME}! "
                              "I can help you download media from various platforms.\n\n"
                              "Here are the available commands:\n"
                              "1. YouTube (PM only): Just send me a YouTube link.\n"
                              "2. Pinterest: Just send me a Pinterest link.\n"
                              "3. Twitter & Facebook: Use /sdl <link> to download.")

# Handlers setup
def main():
    start_handler = CommandHandler('start', start)
    youtube_handler = MessageHandler(Filters.text & Filters.private, youtube_download)
    pinterest_handler = MessageHandler(Filters.text & Filters.regex(r'pinterest\.com'), pinterest_download)
    social_handler = CommandHandler('sdl', social_downloader, pass_args=True)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(youtube_handler)
    dispatcher.add_handler(pinterest_handler)
    dispatcher.add_handler(social_handler)

    # Start the bot
    updater.start_polling()

if __name__ == "__main__":
    main()

# Helper text for the downloader module
__help__ = """
» Available commands for Downloader 

● Youtube Work only in PM
Just send me the link and wait for me to send the post :)

● Pinterest
Just send me the link and wait for me to send the post :)
Example - https://in.pinterest.com/pin/1117455726273676254/

● Twitter and Facebook
For downloading from any supported site like Twitter or Facebook, use /sdl <link>
Example - /sdl https://twitter.com/i/status/1713856915883937995

/⁠ᐠ⁠｡⁠ꞈ⁠｡⁠ᐟ⁠\
"""

__mod_name__ = "Downloader"
