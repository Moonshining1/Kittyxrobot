import os
import subprocess
import sys
from contextlib import suppress
from time import sleep

from telegram import TelegramError, Update
from telegram.error import Unauthorized
from telegram.ext import CallbackContext, CommandHandler

import MukeshRobot
from MukeshRobot import dispatcher
from MukeshRobot.modules.helper_funcs.chat_status import dev_plus


@dev_plus
def allow_groups(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        update.effective_message.reply_text(f"Current state: {MukeshRobot.ALLOW_CHATS}")
        return
    if args[0].lower() in ["off", "no"]:
        MukeshRobot.ALLOW_CHATS = True
    elif args[0].lower() in ["yes", "on"]:
        MukeshRobot.ALLOW_CHATS = False
    else:
        update.effective_message.reply_text("Format: /lockdown Yes/No or Off/On")
        return
    update.effective_message.reply_text("Done! Lockdown value toggled.")


@dev_plus
def leave(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    if args:
        chat_id = str(args[0])
        try:
            bot.leave_chat(int(chat_id))
        except TelegramError:
            update.effective_message.reply_text(
                "Beep boop, I could not leave that group(dunno why tho)."
            )
            return
        with suppress(Unauthorized):
            update.effective_message.reply_text("Beep boop, I left that soup!.")
    else:
        update.effective_message.reply_text("Send a valid chat ID")


@dev_plus
def gitpull(update: Update, context: CallbackContext):
    sent_msg = update.effective_message.reply_text(
        "Pulling all changes from remote and then attempting to restart."
    )
    subprocess.Popen("git pull", stdout=subprocess.PIPE, shell=True)

    sent_msg_text = sent_msg.text + "\n\nChanges pulled...I guess.. Restarting in "

    for i in reversed(range(5)):
        sent_msg.edit_text(sent_msg_text + str(i + 1))
        sleep(1)

    sent_msg.edit_text("Restarted.")

    os.system("restart.bat")
    os.execv("start.bat", sys.argv)


@dev_plus
def restart(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        "Starting a new instance and shutting down this one"
    )

    os.system("restart.bat")
    os.execv("start.bat", sys.argv)


LEAVE_HANDLER = CommandHandler("leave", leave, run_async=True)
GITPULL_HANDLER = CommandHandler("gitpull", gitpull, run_async=True)
RESTART_HANDLER = CommandHandler("reboot", restart, run_async=True)
ALLOWGROUPS_HANDLER = CommandHandler("lockdown", allow_groups, run_async=True)

dispatcher.add_handler(ALLOWGROUPS_HANDLER)
dispatcher.add_handler(LEAVE_HANDLER)
dispatcher.add_handler(GITPULL_HANDLER)
dispatcher.add_handler(RESTART_HANDLER)



__handlers__ = [LEAVE_HANDLER, GITPULL_HANDLER, RESTART_HANDLER, ALLOWGROUPS_HANDLER]

__mod_name__ = "Devs"
__help__ = """
» Available commands for Devs 

● /groups: List gc :)
● /stats: Shows overall bot stats
● /getchats: Gets a common gc for user.
● /ginfo username/link/ID: Pulls info panel for entire group
● /ignore: Blacklists a user from using the bot entirely
● /lockdown <off/on>: Toggles bot adding to groups
● /notice: Removes user from blacklist
● /ignoredlist: Lists ignored users
● /listmodules: List all modules
● /load modulename: Loads the said module to memory without restarting.
● /unload modulename: Loads the said module from memory.
● /debug <on/off>: Logs commands to updates.txt
● /logs: Run this in support group to get logs in pm
● /eval: Self explanatory
● /sh: Runs shell command
● /clearlocals: As the name goes
● /dbcleanup: Removes deleted accs and groups from db
● /py: Runs python code
● /gignoreblue: <word>: Globally ignore.
● /ungignoreblue: <word>: Remove said command from global cleaning list

/⁠ᐠ⁠｡⁠ꞈ⁠｡⁠ᐟ⁠\
"""
