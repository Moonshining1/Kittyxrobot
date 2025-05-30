import requests
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler

from MukeshRobot import CASH_API_KEY, dispatcher


def convert(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(" ")

    if len(args) == 4:
        try:
            orig_cur_amount = float(args[1])

        except ValueError:
            update.effective_message.reply_text("Invalid Amount Of Currency")
            return

        orig_cur = args[2].upper()

        new_cur = args[3].upper()

        request_url = (
            f"https://www.alphavantage.co/query"
            f"?function=CURRENCY_EXCHANGE_RATE"
            f"&from_currency={orig_cur}"
            f"&to_currency={new_cur}"
            f"&apikey={CASH_API_KEY}"
        )
        response = requests.get(request_url).json()
        try:
            current_rate = float(
                response["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
            )
        except KeyError:
            update.effective_message.reply_text("Currency Not Supported.")
            return
        new_cur_amount = round(orig_cur_amount * current_rate, 5)
        update.effective_message.reply_text(
            f"{orig_cur_amount} {orig_cur} = {new_cur_amount} {new_cur}"
        )

    elif len(args) == 1:
        update.effective_message.reply_text(__help__, parse_mode=ParseMode.MARKDOWN)

    else:
        update.effective_message.reply_text(
            f"*Invalid Args!!:* Required 3 But Passed {len(args) -1}",
            parse_mode=ParseMode.MARKDOWN,
        )


__help__ = """
» Available commands for Cash

Converts money from one exchange to another

Usage: /cash amount from to
Example: /cash 20 USD INR

/⁠ᐠ⁠｡⁠ꞈ⁠｡⁠ᐟ⁠\
"""

CONVERTER_HANDLER = CommandHandler("cash", convert, run_async=True)
dispatcher.add_handler(CONVERTER_HANDLER)
__command_list__ = ["cash"]

__handlers__ = [CONVERTER_HANDLER]

__mod_name__ = "Cash"
